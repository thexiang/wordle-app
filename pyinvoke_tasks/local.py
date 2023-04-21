import socket
from contextlib import closing

import questionary
from invoke import task
from rich.console import Console

_CONSOLE = Console(width=200)
DOCKER_RUN = "docker-compose run --rm wordle-helper"


@task
def help(c):
    c.run("inv --list local")


@task
def cleanup(c):
    """delete all docker resources, including containers, images, etc.."""
    is_confirm = questionary.confirm("This will delete all your docker containers and images, please confirm").ask()
    if not is_confirm:
        return

    c.run("sudo rm -rf mongo-data")
    c.run("docker system prune -f")

    num_of_running_containers = c.run("docker ps -aq | wc -l").stdout.strip()
    if int(num_of_running_containers) > 0:
        c.run("docker stop $(docker ps -aq)")

    num_of_images = c.run("docker images -aq | wc -l").stdout.strip()
    if int(num_of_images) > 0:
        c.run("docker rmi $(docker images -aq) -f")

    c.run("docker system prune -f")


@task
def start(c):
    """Run Docker Compose Up"""
    _check_local_ports()
    c.run("docker-compose -f docker-compose.yml up", pty=True)


@task
def unit(c):
    """Run unit tests"""
    c.run(f"{DOCKER_RUN} pytest -vvvsx wordle/tests/unit/ --cov=wordle", pty=True)


@task
def integration(c):
    """Run integration tests"""
    c.run(f"{DOCKER_RUN} pytest -vvvsx wordle/tests/integration/ --cov=wordle", pty=True)


@task
def test(c):
    """Run All tests"""
    c.run(f"{DOCKER_RUN} pytest -vvvsx wordle/tests/ --cov=wordle", pty=True)


@task
def shell(c):
    """Start a shell in a container within the docker-compose network"""
    c.run("docker-compose run --rm -it --entrypoint bash wordle-helper", pty=True)


@task
def lint(c):
    """black, lint, ruff"""
    c.run(f"{DOCKER_RUN} black .", pty=True)
    c.run(f"{DOCKER_RUN} isort .", pty=True)
    c.run(f"{DOCKER_RUN} ruff --fix .", pty=True)


def _check_local_ports():
    require_local_ports = [8000, 27017]
    for port in require_local_ports:
        _is_port_available(port)


def _is_port_available(port, host='localhost'):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            _CONSOLE.print(f'❌ Port {port} is in use, please free up ports, exiting program')
            exit(0)
        else:
            print(f'✅ Port {port} is available')
