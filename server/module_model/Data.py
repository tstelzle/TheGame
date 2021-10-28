import datetime

from module_model.Game import Game, GameSchema
from pymongo.errors import PyMongoError

GAMES = []


def get_game(game_id: str):
    for game in GAMES:
        if str(game["id"]) == game_id:
            return game["game"], True

    return None, False


def store_games():
    print("store_games")
    now = datetime.datetime.now(datetime.timezone.utc)
    for game_item in GAMES:
        game = game_item["game"]
        duration = now - game.last_updated
        if int(duration.total_seconds()) > 86400:
            try:
                game_schema = GameSchema()
                game.mongo_id = game.collection.insert_one(game_schema.dump(game)).inserted_id
                print("Storing Game", game.game_id, "in Mongo as", game.mongo_id)
            except PyMongoError:
                print("Could not store game", game.game_id)
