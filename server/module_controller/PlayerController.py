import json
from flask_restful import Resource


class PlayerController(Resource):

    def put(self, name: str):
        return json.dumps("Created Player " + name)
