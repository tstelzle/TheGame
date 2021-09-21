from flask import jsonify
from flask_restful import Resource

from module_model import Data, Game, Player
from app import app


class PlayerController(Resource):

    @staticmethod
    @app.route("/player/<game_uid>/<name>", methods=["POST"])
    def add_player(game_uid: str, name: str):
        player = Player(name)
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401
        game.add_player(player)
        for i in range(game.starting_cards):
            game.handout_card(player)

        return jsonify(isError=False,
                       message="CREATED",
                       statusCode=201,
                       data=str(player.player_id)), 201
