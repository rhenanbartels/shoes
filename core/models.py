from decouple import config

from pymongo import MongoClient


client = MongoClient(
        config('MONGO_ADDR'),
        config('MONGO_PORT', cast=int)
)
