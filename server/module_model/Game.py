from module_model.Player import Player
from module_model.Pile import Pile
from module_model.Deck import Deck
from module_model.GameStatus import GameStatus


class Game:

    def __init__(self, name: str, game_id: int, starting_cards = 5):
        self.game_id = game_id
        self.name = name
        self.players = []
        self.piles = self.initialize_piles()
        self.deck = self.create_deck()
        self.starting_cards = starting_cards
        self.current_player = 0
        self.cards_to_play = 2
        self.cards_played = 0
        self.state = GameStatus.INITIALIZE

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
