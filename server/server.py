import module_controller
import pymongo

from app import api, app

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)

DOMAIN = "localhost"
PORT = "27000"

def create_database_connection() -> pymongo.MongoClient:
    myclient = pymongo.MongoClient(
        host= [ str(DOMAIN) + ":" + str(PORT)]
    )

    print(myclient.server_info())

    return myclient

def setup_database(myclient: pymongo.MongoClient, database_name = "thegame_db"):
    return myclient[database_name]

def create_collection(collection_name: str, mydb):
    return mydb[collection_name]

if __name__ == "__main__":
    myclient = create_database_connection()
    database = setup_database(myclient)
    collection = create_collection('games', database)

    test_dict = {'name': 'test_name', 'uid': 'game_uid'}

    collection.insert_one(test_dict)
    print('test')
    app.run(host="0.0.0.0", port=5050)
