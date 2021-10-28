from marshmallow import Schema, fields, post_load


class Pile:

    def __init__(self, top_card: int):
        self.top_card = top_card


class PileSchema(Schema):
    top_card = fields.Integer()

    @post_load
    def make_store(self, data, **kwargs):
        return Pile(**data)
