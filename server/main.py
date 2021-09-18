from flask import Flask
from flask_restful import Api
from module_controller import *

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

api.add_resource(GameController, "/game/<string:name>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
