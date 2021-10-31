import pymongo
import pymongo.errors
import pymongo.database
import pymongo.collection
import time
import os

DATABASE_CLIENT = pymongo.MongoClient()
GAME_COLLECTION = pymongo.collection.Collection
PLAYER_COLLECTION = pymongo.collection.Collection


def create_database_connection() -> None:
    global DATABASE_CLIENT
    user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    db_container = os.getenv('DB_CONTAINER')

    connection_url = "mongodb://{0}:{1}@{2}:27017".format(user, password, db_container)

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


def get_game(game_uid: str):
    record = GAME_COLLECTION.find_one({"game_id": game_uid}, {"_id": 0})

    return record


def get_games(game_uid: str):
    records = GAME_COLLECTION.find({"game_id": game_uid})

    return records


def update_game(game: dict):
    updated_game = GAME_COLLECTION.update_one({"game_id": game["game_id"]}, {"$set": game}, upsert=True)

    return updated_game.upserted_id


def delete_games(game_uid: str) -> int:
    delete_count = GAME_COLLECTION.delete_many({"game_id": game_uid})

    return delete_count.deleted_count


def setup_database():
    global GAME_COLLECTION
    global PLAYER_COLLECTION
    create_database_connection()
    game_database = create_database(DATABASE_CLIENT)
    GAME_COLLECTION = create_collection('games', game_database)
