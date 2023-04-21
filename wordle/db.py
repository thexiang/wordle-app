from pymongo import MongoClient
from pymongo.collection import Collection

from .config import wordle_settings

client = MongoClient(wordle_settings.wordle_db_url.get_secret_value())
db_collection: Collection = client[wordle_settings.mongo_database][wordle_settings.mongo_collection]
