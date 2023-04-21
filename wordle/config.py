import logging

from pydantic import BaseSettings
from pydantic import SecretStr

log = logging.getLogger("uvicorn")


class WordleSettings(BaseSettings):
    environment: str = "dev"
    # TODO, This is hard coded for current local docer-compose setup, clean it up later
    mongo_user: str = "mantium"
    mongo_host: str = "wordle-db"
    mongo_port: str = "27017"
    mongo_database: str = "wordle"
    mongo_password: SecretStr = "password"
    mongo_collection: str = "games"

    @property
    def wordle_db_url(self):
        return SecretStr(
            f"mongodb://{self.mongo_user}:{self.mongo_password.get_secret_value()}@{self.mongo_host}:{self.mongo_port}/{self.mongo_database}"
        )


wordle_settings = WordleSettings()
