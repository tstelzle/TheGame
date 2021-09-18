from module_model.Player import Player
from module_model.Pile import Pile
from module_model.Deck import Deck


class Game:

    def __init__(self, name: str, game_id: int):
        self.game_id = game_id
        self.name = name
        self.players = []
        self.piles = self.initialize_piles()
        self.deck = self.create_deck()

    @staticmethod
    def initialize_piles():
        pile_1_1 = Pile(1)
        pile_1_2 = Pile(2)
        pile_100_1 = Pile(100)
        pile_100_2 = Pile(100)

        return [pile_1_1, pile_1_2, pile_100_1, pile_100_2]

    @staticmethod
    def create_deck():
        deck = Deck()

        return deck

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        p = [p for p in self.players if p.name == player.name][0]
        self.players.remove(p)
