from pydantic import BaseModel
from pydantic.types import constr


class GuessRequest(BaseModel):
    game_id: constr(min_length=6, max_length=6)
    word: constr(min_length=5, max_length=5)
