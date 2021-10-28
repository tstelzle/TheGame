from json import dumps, loads

import pymongo
import pymongo.errors
import pymongo.database
import pymongo.collection
import time
import os
from module_model import Game

DATABASE_CLIENT = pymongo.MongoClient()
GAME_COLLECTION = pymongo.collection.Collection
PLAYER_COLLECTION = pymongo.collection.Collection

def create_database_connection() -> None:
    global DATABASE_CLIENT
    user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

    connection_url = "mongodb://{0}:{1}@thegame-db:27017".format(user, password)

    connection_not_established = True
    while connection_not_established:
        try:
            DATABASE_CLIENT = pymongo.MongoClient(connection_url)
            connection_not_established = False
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Timeout Error - Waiting and Retrying")
            time.sleep(5)

    print("server version:", DATABASE_CLIENT.server_info()["version"])


def create_database(database_client: pymongo.MongoClient, database_name="thegame_db") -> pymongo.database.Database:
    return database_client[database_name]


def create_collection(collection_name: str, database: pymongo.database.Database) -> pymongo.collection.Collection:
    return database[collection_name]

def get_game(game_uid: str) -> Game:
    record = GAME_COLLECTION.find({"uid": game_uid})
    game_json = dumps(record)

    return loads(game_json)

def setup_database():
    global GAME_COLLECTION
    global PLAYER_COLLECTION
    create_database_connection()
    game_database = create_database(DATABASE_CLIENT)
    GAME_COLLECTION = create_collection('games', game_database)
    # PLAYER_COLLECTION = create_collection('players', game_database)
