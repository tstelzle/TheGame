import module_controller

from app import api, app
import database_connection

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)


if __name__ == "__main__":
    database_connection.setup_database()
    app.run(host="0.0.0.0", port=5050)
