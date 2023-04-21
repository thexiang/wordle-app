from pydantic import BaseModel


class Guess(BaseModel):
    guess_result: str
    incorrectly_guessed_letters: list[str]
    letter1: str
    letter2: str
    letter3: str
    letter4: str
    letter5: str


class Game(BaseModel):
    game_id: str
    target_word: str
    guesses: list[Guess] = []
    num_of_round: int = 0
    correct_letters: list[str] = []
    incorrect_letters: list[str] = []
    wrong_position_letters: list[str] = []
    is_win: bool = False
