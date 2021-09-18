from flask_restful import Resource

from module_model import Data, Game, Player
from app import app

class PlayerController(Resource):

    @staticmethod
    @app.route("/player/<game_id>/<name>", methods=["POST"])
    def add_player(game_id: str, name: str):
        player = Player(name)

        searched_game = None

        for game in Data.GAMES:
            if str(game["id"]) == game_id:
                searched_game = game["game"]

        if searched_game is None:
            raise Exception("Game Not Found.")

        searched_game.add_player(player)

        return player.name + "; " + str(player.player_id), 201
