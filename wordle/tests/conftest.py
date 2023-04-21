import mongomock
import pytest
from starlette.testclient import TestClient

from wordle.models.game_model import Game
from wordle.server import create_application


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def unit_db_client_mock():
    yield mongomock.MongoClient()


@pytest.fixture
def unit_db_mock(unit_db_client_mock):
    yield unit_db_client_mock.db


@pytest.fixture
def wordle_collection_mock(unit_db_mock):
    yield unit_db_mock.collection


@pytest.fixture
def mock_game():
    return Game(game_id="test01", target_word="DOJOS")
