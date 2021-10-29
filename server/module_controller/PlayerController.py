from flask import jsonify
from flask_restful import Resource

from module_model import Data, Player
from app import app


class PlayerController(Resource):

    @staticmethod
    @app.route("/api/player/piles/<game_uid>", methods=["GET"])
    def get_piles(game_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401
        top_cards = game.get_piles_topcard()

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=top_cards), 200

    @staticmethod
    @app.route("/api/players/<game_uid>", methods=["GET"])
    def get_players(game_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401

        player_names = [player.name for player in game.players]

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=(player_names, game.current_player)), 200

    @staticmethod
    @app.route("/api/player/valid/<game_uid>/<player_uid>", methods=["GET"])
    def is_player_valid(game_uid: str, player_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401
        for player in game.players:
            if str(player.player_id) == player_uid:
                return jsonify(isError=False,
                               message="SUCCESS",
                               statusCode=200,
                               data=player.hand_cards), 200

        return jsonify(isError=True,
                       message="ERROR",
                       statusCode=400,
                       data=""), 400

    @staticmethod
    @app.route("/api/player/<game_uid>/<player_id>", methods=["GET"])
    def get_handcards(game_uid: str, player_id: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401

        player = game.get_player(player_id)

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=player.hand_cards), 200

    @staticmethod
    @app.route("/api/player/<game_uid>/<name>", methods=["POST"])
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
