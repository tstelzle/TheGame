import uuid

from flask_restful import Resource
from module_model import Data, Game
from app import app


class GameController(Resource):

    @staticmethod
    @app.route("/game/<name>", methods=["POST"])
    def add_game(name: str):
        game_uid = uuid.uuid1()
        game = Game(name, game_uid)

        Data.GAMES.append({"id": game_uid, "game": game})

        return str(game_uid), 201

    @staticmethod
    @app.route("/game/<game_uid>", methods=["GET"])
    def get_game(game_uid: str):
        searched_game = None
        for game in Data.GAMES:
            if str(game["id"]) == game_uid:
                searched_game = game

        if searched_game is None:
            raise Exception("Game Not Found")

        return searched_game["game"].name, 201
