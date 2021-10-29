import uuid

from marshmallow import Schema, fields, post_load


class Player:

    def __init__(self, name: str, player_id=None, hand_cards=[]):
        self.name = name
        self.player_id = player_id if player_id else uuid.uuid1()
        self.hand_cards = hand_cards

    def add_card(self, card: int):
        self.hand_cards.append(card)


class PlayerSchema(Schema):
    name = fields.Str()
    player_id = fields.Str()
    hand_cards = fields.List(fields.Integer())

    @post_load
    def make_player(self, data, **kwargs):
        return Player(**data)
