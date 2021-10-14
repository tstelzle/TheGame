from pymongo.errors import PyMongoError

GAMES = []


def get_game(game_id: str):
    for game in GAMES:
        if str(game["id"]) == game_id:
            return game["game"], True

    return None, False


def store_games():
    print("store_games")
    for game_item in GAMES:
        game = game_item["game"]
        game_dic = game.as_dic()
        try:
            game.mongo_id = game.collection.insert_one(game_dic).inserted_id
            print("Storing Game", game.game_id, "in Mongo as", game.mongo_id)
        except PyMongoError:
            print("Could not store game", game.game_id)
