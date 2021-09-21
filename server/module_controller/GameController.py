import uuid

from app import app
from flask import jsonify
from flask_cors import cross_origin
from flask_restful import Resource
from module_model import Data, Game, GameStatus


class GameController(Resource):

    @staticmethod
    @app.route("/player/<game_uid>/<player_id>", methods=["GET"])
    @cross_origin()
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
    @app.route("/player/valid/<game_uid>/<player_uid>", methods=["GET"])
    @cross_origin()
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
    @app.route("/game/<name>", methods=["POST"])
    @cross_origin()
    def add_game(name: str):
        # TODO Check if game with name already exists -> but not really necessary as of uid
        game_uid = uuid.uuid1()
        game = Game(name, game_uid)

        Data.GAMES.append({"id": game_uid, "game": game})

        return jsonify(isError=False,
                       message="CREATED",
                       statusCode=201,
                       data=str(game_uid)), 201

    @staticmethod
    @app.route("/players/<game_uid>", methods=["GET"])
    @cross_origin()
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
    @app.route("/game/currentPlayer/<game_uid>", methods=["GET"])
    @cross_origin()
    def get_current_player(game_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401
        player = game.get_current_player()

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=player.player_id), 200

    @staticmethod
    @app.route("/game/<game_uid>", methods=["GET"])
    @cross_origin()
    def get_game(game_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401

        return jsonify(isError=False,
                       message="CREATED",
                       statusCode=201,
                       data=str(game.name)), 201

    @staticmethod
    @app.route("/game/<game_uid>/<player_id>/<pile_id>/<card>", methods=["POST"])
    @cross_origin()
    def play_card(game_uid: str, player_id: str, pile_id: str, card: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401
        player = game.get_player(player_id)
        current_player_id = str(game.get_current_player().player_id)
        pile_id = int(pile_id)
        card = int(card)
        if player_id != current_player_id:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=400,
                           data="Not Your Turn"), 400

        pile = game.get_pile(int(pile_id))
        top_card = pile.top_card
        card_accepted = False
        if pile_id == 0 or pile_id == 1:
            if card > top_card:
                card_accepted = True
            elif card + 10 == top_card:
                card_accepted = True

        if pile_id == 2 or pile_id == 3:
            if card < top_card:
                card_accepted = True
            elif card - 10 == top_card:
                card_accepted = True

        if card_accepted:
            player.hand_cards.remove(card)
            pile.top_card = card
            game.cards_played += 1
            return jsonify(isError=False,
                           message="SUCCESS",
                           statusCode=200,
                           data=pile.top_card), 200

        return jsonify(isError=True,
                       message="ERROR",
                       statusCode=400,
                       data="Card Not Accepted"), 400

    @staticmethod
    @app.route("/game/<game_uid>/<player_id>", methods=["POST"])
    @cross_origin()
    def end_turn(game_uid: str, player_id: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401

        if game.cards_played < game.cards_to_play:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=400,
                           data="Missing Cards"), 400

        game.cards_played = 0
        player = game.get_player(player_id)
        game.current_player = game.get_next_player_id()
        while len(player.hand_cards) < game.starting_cards:
            if len(game.deck.cards) > 0:
                game.handout_card(player)
            else:
                game.cards_to_play = 1

        game.check_win()

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=""), 200

    @staticmethod
    @app.route("/game/state/<game_uid>", methods=["GET"])
    @cross_origin()
    def get_game_state(game_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=400,
                           data=""), 400

        return jsonify(isError=False,
                       message="SUCCESS",

                       statusCode=200,
                       data=game.state.value), 200

    @staticmethod
    @app.route("/game/state/<game_uid>/<state>", methods=["POST"])
    @cross_origin()
    def set_game_state(game_uid: str, state: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401

        game.state = GameStatus(state)

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=""), 200

    @staticmethod
    @app.route("/player/piles/<game_uid>", methods=["GET"])
    @cross_origin()
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
    @app.route("/game/deck/<game_uid>", methods=["GET"])
    @cross_origin()
    def get_cards(game_uid: str):
        game, game_status = Data.get_game(game_uid)
        if not game_status:
            return jsonify(isError=True,
                           message="ERROR",
                           statusCode=401,
                           data=""), 401

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=len(game.deck.cards)), 200
