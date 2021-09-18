import uuid


class Player:

    def __init__(self, name: str):
        self.name = name
        self.player_id = uuid.uuid1()
