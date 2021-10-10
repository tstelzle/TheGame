import module_controller
import pymongo
import time
import os

from app import api, app

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)


def create_database_connection() -> pymongo.MongoClient:
    USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

    CONNECTION_URL = "mongodb://{0}:{1}@thegame-db:27017".format(USER, PASSWORD)

    connection_not_established = True
    while connection_not_established:
        try:
            myclient = pymongo.MongoClient(CONNECTION_URL)
            connection_not_established = False
        except Exception:
            print("Timeout Error - Waiting and Retrying")
            time.sleep(5)

    print("server version:", myclient.server_info()["version"])

    return myclient

def setup_database(myclient: pymongo.MongoClient, database_name = "thegame_db"):
    return myclient[database_name]

def create_collection(collection_name: str, mydb):
    return mydb[collection_name]

if __name__ == "__main__":
    print("main")
    myclient = create_database_connection()
    database = setup_database(myclient)
    collection = create_collection('games', database)

    test_dict = {'name': 'test_name', 'uid': 'game_uid'}

    collection.insert_one(test_dict)
    print('test')
    app.run(host="0.0.0.0", port=5050)
