from flask_cors import CORS
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
CORS(app)
api = Api(app)
