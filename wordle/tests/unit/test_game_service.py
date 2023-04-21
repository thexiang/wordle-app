from copy import deepcopy

import pytest

from wordle.exceptions import GameNotFound
from wordle.models.game_model import Guess
from wordle.services.game_service import GameService


def test_db_get_game_empty_db(wordle_collection_mock, mock_game):
    service = GameService()
    with pytest.raises(GameNotFound):
        service.db_get_game(wordle_collection_mock, mock_game.game_id)


def test_db_add_game_and_db_get_game(wordle_collection_mock, mock_game):
    service = GameService()
    service.db_add_game(wordle_collection_mock, mock_game)
    result = service.db_get_game(wordle_collection_mock, mock_game.game_id)
    assert result == mock_game


def test_db_update_game(wordle_collection_mock, mock_game):
    service = GameService()
    # make a copy of original game
    mock_game_copy = deepcopy(mock_game)
    service.db_add_game(wordle_collection_mock, mock_game)

    # the new game object has a is_win value
    mock_game_copy.is_win = True

    # update the original game document in db with the new game object
    service.db_update_game(wordle_collection_mock, mock_game.game_id, mock_game_copy)

    # proving the document has been updated
    mock_game_after_update = service.db_get_game(wordle_collection_mock, mock_game.game_id)
    assert mock_game.is_win != mock_game_after_update.is_win


def test_get_game(mock_game, mocker):
    service = GameService()
    mocker.patch('wordle.services.game_service.GameService.db_get_game', return_value=mock_game)
    subject = service.get_game(mock_game.game_id)
    assert subject == mock_game


def test__handle_guess(mock_game):
    service = GameService()
    # correct word is DOJOS
    guess = service._handle_guess(mock_game, "DIDOS")

    assert guess == Guess(
        guess_result="incorrect",
        incorrectly_guessed_letters=["I"],
        letter1="correct",
        letter2="incorrect",
        letter3="wrong_position",
        letter4="correct",
        letter5="correct",
    )
