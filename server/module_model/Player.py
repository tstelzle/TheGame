import uuid


class Player:

    def __init__(self, name: str):
        self.name = name
        self.player_id = uuid.uuid1()
        self.hand_cards = []

    def add_card(self, card: int):
        self.hand_cards.append(card)