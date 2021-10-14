import module_controller

from app import api, app

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)

application = app
