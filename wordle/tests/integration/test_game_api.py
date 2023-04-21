import pytest

from wordle.db import db_collection
from wordle.services.game_service import GameService


@pytest.fixture
def new_game_id_fixture(test_app):
    response = test_app.post("/new_game")
    assert response.status_code == 200
    data = response.json()
    game_id = data["game_id"]
    yield game_id
    # clean up
    service = GameService()
    service.db_delete_game(db_collection, data["game_id"])


def test_new_game_api(test_app):
    response = test_app.post("/new_game")
    assert response.status_code == 200
    data = response.json()
    # game_id always has length 6
    assert "game_id" in data
    # game_id always has length 6
    assert len(data["game_id"]) == 6

    # clean up
    service = GameService()
    service.db_delete_game(db_collection, data["game_id"])


def test_guess_api_success(test_app, new_game_id_fixture):
    response = test_app.post("/guess", json={"game_id": new_game_id_fixture, "word": "APPLE"})
    assert response.status_code == 200
    expected_keys = [
        "guess_result",
        "incorrectly_guessed_letters",
        "incorrectly_guessed_letters",
        "letter1",
        "letter2",
        "letter3",
        "letter4",
        "letter5",
    ]
    assert all(key in expected_keys for key in response.json())


@pytest.mark.parametrize(
    "game_id, word, msg",
    [
        ('123', 'APPLE', "ensure this value has at least 6 characters"),
        ('1234567', 'APPLE', "ensure this value has at most 6 characters"),
        ('abcdef', 'ABC', "ensure this value has at least 5 characters"),
        ('abcdef', 'ABCDEFG', "ensure this value has at most 5 characters"),
    ],
    ids=["short game_id", "long game_id", "short word", "long word"],
)
def test_guess_api_fail_on_paylod_validation(test_app, game_id, word, msg):
    response = test_app.post("/guess", json={"game_id": game_id, "word": word})
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == msg
    print(response.json())


def test_guess_api_fail_on_invalid_word(test_app, new_game_id_fixture):
    response = test_app.post("/guess", json={"game_id": new_game_id_fixture, "word": "AAAAA"})
    assert response.status_code == 200
    assert response.json() == {'guess_result': 'invalid'}
