import uuid


class Player:

    def __init__(self, name: str):
        self.name = name
        self.player_id = uuid.uuid1()
        self.hand_cards = []

    def add_card(self, card: int):
        self.hand_cards.append(card)

    def as_dic(self) -> dict:
        return {
            "name": self.name,
            "uid": str(self.player_id),
            "hand_cards": self.hand_cards
        }
