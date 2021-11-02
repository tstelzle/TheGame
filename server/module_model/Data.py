import datetime

from module_model.Game import Game, GameSchema
from pymongo.errors import PyMongoError
import database_connection
import logger

GAMES = []


def get_game(game_id: str):
    found_game = None

    for game in GAMES:
        if str(game["id"]) == game_id:
            found_game = game["game"]

    if not found_game:
        mongo_request = database_connection.get_game(game_id)
        if mongo_request:
            game_schema = GameSchema()
            found_game = game_schema.load(mongo_request)
            GAMES.append({"id": found_game.game_id, "game": found_game})
            logger.log_debug("Fetched Game " + found_game.game_id + " from database.")

    if found_game:
        return found_game, True

    return None, False


def store_games():
    logger.log_debug("store_games")
    now = datetime.datetime.now(datetime.timezone.utc)
    removable_games = []
    for game_item in GAMES:
        game = game_item["game"]
        duration = now - game.last_updated
        if int(duration.total_seconds()) > 86400:
            try:
                recorded_games = database_connection.get_games(game.game_id)
                recorded_games_count = recorded_games.count()
                game_schema = GameSchema()

                if recorded_games_count == 1 or recorded_games_count == 0:
                    inserted_id = database_connection.update_game(game_schema.dump(game))
                else:
                    logger.log_debug("Found " + recorded_games_count + " games to be updated.")
                    inserted_id = database_connection.update_game(game_schema.dump(game))

                logger.log_debug("Storing Game " + game.game_id + " in Mongo as " + inserted_id)
                removable_games.append(game_item)
            except PyMongoError:
                logger.log_debug("Could not store game " + game.game_id)

    for game in removable_games:
        GAMES.remove(game)
