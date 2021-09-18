import module_controller

from app import api, app

api.add_resource(module_controller.GameController)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
