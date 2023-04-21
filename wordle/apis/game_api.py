from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse

from wordle.api_schemas.game_api_schema import GuessRequest
from wordle.exceptions import InvalidWord
from wordle.services.game_service import GameService

game = APIRouter()


@game.get("/games/{game_id}")
def get_game(game_id: str):
    service = GameService()
    game = service.get_game(game_id)
    return {"status": "Ok", "data": game}


@game.post("/new_game")
def create_game():
    service = GameService()
    game_id = service.create_game()
    return {"game_id": game_id}


@game.post("/guess")
def make_guess(guess: GuessRequest):
    service = GameService()
    try:
        result = service.make_guess(game_id=guess.game_id, guess_word=guess.word)
    except InvalidWord:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"guess_result": "invalid"})

    return result
