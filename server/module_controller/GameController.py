import json
from flask_restful import Resource


class GameController(Resource):

    def get(self, name: str):
        # TODO Create Game
        print(name)
        return json.dumps("Created Game " + name)
