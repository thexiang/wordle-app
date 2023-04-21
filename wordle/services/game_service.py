import random
import string

from wordle.db import db_collection
from wordle.exceptions import AlreadyEndedGame
from wordle.exceptions import DBError
from wordle.exceptions import GameNotFound
from wordle.exceptions import InvalidWord
from wordle.models.game_model import Game
from wordle.models.game_model import Guess
from wordle.utils import read_list_of_words


class GameService:
    def __init__(self):
        pass

    def db_get_game(self, collection, game_id):
        """DB interface to get game name"""
        try:
            game_document = collection.find_one({"game_id": game_id})
        except:  # noqa: E722
            raise DBError()
        if not game_document:
            raise GameNotFound()
        game = Game(**game_document)
        return game

    def db_add_game(self, collection, game: Game):
        """DB interface to add game name"""
        collection.insert_one(game.dict())

    def db_update_game(self, collection, game_id, new_document):
        """DB interface to update game name"""
        collection.update_one({"game_id": game_id}, {"$set": new_document.dict()})

    def db_delete_game(self, collection, game_id):
        """DB interface to delete game name"""
        collection.delete_one({"game_id": game_id})

    def get_game(self, game_id):
        game = self.db_get_game(db_collection, game_id)
        return game

    def create_game(self):
        """We generate a random 6 digit hex number, and create a new game in DB"""
        game_id = self._generate_game_id()
        target_words, word_count = read_list_of_words()
        index = random.randint(0, word_count)
        game = Game(game_id=game_id, target_word=target_words[index])
        self.db_add_game(db_collection, game)
        return game_id

    def _generate_game_id(self):
        return "".join(random.sample(string.ascii_lowercase, 6))

    def make_guess(self, game_id, guess_word):
        """this is the entry point of the make guess logic, it'll delegate the subtasks to other internal methods"""
        game = self.db_get_game(db_collection, game_id)
        if not game:
            raise
        if game.num_of_round >= 5:
            raise AlreadyEndedGame()
        if game.is_win:
            raise AlreadyEndedGame()

        guess: Guess = self._handle_guess(game, guess_word)
        self._update_game_after_make_guess(game, guess, guess_word)
        return guess

    def _handle_guess(self, game: Game, guess_word: str):
        """
        This method handles guess logic, it'll assign "correct","wrong_position",or "incorrect" to each letter of the word
        """
        if not self.is_valid_word(guess_word):
            raise InvalidWord("please provide a valid word")

        answer = game.target_word
        incorrect_guessed_letters_set = set()
        guess = {}

        # the word is always letters in wordle, we loop through it and compare with the answer.
        for i in range(5):
            letter_key = f"letter{i+1}"
            if answer[i] == guess_word[i]:
                guess[letter_key] = "correct"
            elif guess_word[i] in answer:
                guess[letter_key] = "wrong_position"
            else:
                guess[letter_key] = "incorrect"
                incorrect_guessed_letters_set.add(guess_word[i])
        guess["incorrectly_guessed_letters"] = sorted(list(incorrect_guessed_letters_set))

        # determine if it's correct or wrong, the reason we don't check it at begining, it's because even it's correct, I still want to return the same format of the JSON response in API
        if answer == guess_word:
            guess["guess_result"] = "correct"
        else:
            guess["guess_result"] = "incorrect"
        guess_model = Guess(**guess)
        return guess_model

    def _update_game_after_make_guess(self, game: Game, guess: Guess, guess_word):
        """
        This method will update & store the game board into database.
        """
        answer = game.target_word
        for i in range(5):
            # the reason I didn't use set() to deduplicate is because pydantic .dict() doesn't natively supports set
            if answer[i] == guess_word[i]:
                if guess_word[i] in game.correct_letters:
                    continue
                game.correct_letters.append(guess_word[i])
                # we need remove the wrong position letters when it's in the correct place
                if guess_word[i] in game.wrong_position_letters:
                    game.wrong_position_letters.remove(guess_word[i])
            elif guess_word[i] in answer:
                if guess_word[i] in game.wrong_position_letters:
                    continue
                game.wrong_position_letters.append(guess_word[i])
            else:
                if guess_word[i] in game.incorrect_letters:
                    continue
                game.incorrect_letters.append(guess_word[i])
        game.num_of_round += 1
        game.guesses.append(guess)
        self.db_update_game(db_collection, game.game_id, game)

    def is_valid_word(self, word):
        """
        check if the word is in the words list
        """
        target_words, _ = read_list_of_words()
        if word not in target_words:
            return False
        return True
