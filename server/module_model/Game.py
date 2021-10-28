from module_model.Player import Player, PlayerSchema
from module_model.Pile import Pile, PileSchema
from module_model.Deck import Deck, DeckSchema
from module_model.GameStatus import GameStatus

import database_connection
import datetime
from marshmallow import Schema, fields, post_load


class Game:

    def __init__(self, game_id: int, name: str, players=[], piles=None, deck=None, starting_cards=5, current_player=0, cards_to_play=2, cards_played=0, state= GameStatus.INITIALIZE):
        self.game_id = game_id
        self.name = name
        self.players = players
        self.piles = piles if piles else self.initialize_piles()
        self.deck = deck if deck else self.create_deck()
        self.starting_cards = starting_cards
        self.current_player = current_player
        self.cards_to_play = cards_to_play
        self.cards_played = cards_played
        self.state = state
        self.collection = database_connection.GAME_COLLECTION
        self.mongo_id = ""
        self.last_updated = datetime.datetime.now(datetime.timezone.utc)

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def get_next_player(self) -> Player:
        self.current_player = (self.current_player + 1) % len(self.players)
        return self.players[self.current_player]

    def get_next_player_id(self) -> int:
        self.current_player = (self.current_player + 1) % len(self.players)
        return self.current_player

    @staticmethod
    def initialize_piles() -> [Pile]:
        pile_1_1 = Pile(1)
        pile_1_2 = Pile(1)
        pile_100_1 = Pile(100)
        pile_100_2 = Pile(100)

        return [pile_1_1, pile_1_2, pile_100_1, pile_100_2]

    @staticmethod
    def create_deck() -> Deck:
        deck = Deck()

        return deck

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def remove_player(self, player: Player) -> None:
        p = [p for p in self.players if p.name == player.name][0]
        self.players.remove(p)

    def handout_card(self, player: Player) -> None:
        new_card = self.deck.handout_card()
        player.add_card(new_card)

    def get_pile(self, pile_id: int) -> Pile:
        return self.piles[pile_id]

    def get_player(self, player_id: int) -> Player:
        for player in self.players:
            if str(player.player_id) == player_id:
                return player

        raise Exception("Player Not Found.")

    def get_piles_topcard(self):
        top_cards = []
        for pile in self.piles:
            top_cards.append(pile.top_card)

        return top_cards

    def check_win(self):
        if len(self.deck.cards) == 0:
            amount_handcards = sum([len(player.hand_cards) for player in self.players])
            if amount_handcards == 0:
                self.win_state = GameStatus.WIN
                return True

        return False


class GameSchema(Schema):
    game_id = fields.Str()
    name = fields.Str()
    players = fields.List(fields.Nested(PlayerSchema))
    piles = fields.List(fields.Nested(PileSchema))
    deck = fields.Nested(DeckSchema)
    starting_cards = fields.Integer()
    current_player = fields.Integer()
    cards_to_play = fields.Integer()
    cards_played = fields.Integer()
    state = fields.Str()
    last_updated = fields.DateTime()

    @post_load
    def make_store(self, data, **kwargs):
        return Game(**data)
