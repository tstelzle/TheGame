import random

from marshmallow import Schema, fields, post_load


class Deck:

    def __init__(self, cards=[]):
        self.cards = cards if cards else list(range(2, 99))
        self.mix_cards()

    def mix_cards(self):
        random.shuffle(self.cards)

    def handout_card(self):
        return self.cards.pop(0)


class DeckSchema(Schema):
    cards = fields.List(fields.Integer())

    @post_load
    def make_deck(self, data, **kwargs):
        return Deck(**data)
