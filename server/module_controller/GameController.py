import uuid

from flask import jsonify
from flask_restful import Resource
from module_model import Data, Game
from app import app


class GameController(Resource):

    @staticmethod
    @app.route("/game/<name>", methods=["POST"])
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
    def get_players(game_uid: str):
        game = Data.get_game(game_uid)

        player_names = [player.name for player in game.players]

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=player_names), 200

    @staticmethod
    @app.route("/game/currentPlayer/<game_uid>", methods=["GET"])
    def get_current_player(game_uid: str):
        game = Data.get_game(game_uid)
        player = game.get_current_player()

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=player.player_id), 200


    @staticmethod
    @app.route("/game/<game_id>", methods=["GET"])
    def get_game(game_id: str):
        game = Data.get_game(game_id)

        return jsonify(isError=False,
                       message="CREATED",
                       statusCode=201,
                       data=str(game.name)), 201

    @staticmethod
    @app.route("/game/state/<game_uid>", methods=["GET"])
    def game_state(game_uid: str):
        game = Data.get_game(game_uid)

        return jsonify(isError=False,
                       message="SUCCESS",
                       statusCode=200,
                       data=str(game.state))

    @staticmethod
    @app.route("/game/state/<game_uid>", methods=["POST"])
    def set_state(game_uid: str):
        game = Data.get_game(game_uid)
        game.state = True

        return jsonify(isError=False,
                       message="CREATED",
                       statusCode=201,
                       data=str(game.state))
    @staticmethod
    @app.route("/game/<game_id>/<player_id>/<pile_id>/<card>", methods=["POST"])
    def play_card(game_id: str, player_id: str, pile_id: int, card: int):
        game = Data.get_game(game_id)
        player = game.get_player(player_id)
        if player != game.get_current_player():
            return "Not Your Turn", 400
        pile = game.get_pile(pile_id)
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
            return 200

        return "Card Not Placeable", 400

    @staticmethod
    @app.route("/game/<game_id>/<player_id>", methods=["POST"])
    def end_turn(game_id: str, player_id: str):
        game = Data.get_game(game_id)
        player = game.get_player(player_id)
        while len(player.hand_cards) < game.starting_cards:
            if len(game.deck.cards) > 0:
                game.handout_card(player)

    @staticmethod
    @app.route("/player/<game_id>/<player_id>", methods=["GET"])
    def get_handcards(game_id: str, player_id: str):
        game = Data.get_game(game_id)
        player = game.get_player(player_id)

        return player.hand_cards, 200
