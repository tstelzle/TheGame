import module_controller
import os

from app import api, app
import database_connection
from apscheduler.schedulers.background import BackgroundScheduler
import logger

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)

database_connection.setup_database()

scheduler = BackgroundScheduler()
scheduler.add_job(func=module_controller.Data.store_games, trigger="interval", hours=12)
scheduler.start()

logger.create_logger("./log_file.txt")

server_environment = os.getenv('SERVER_ENVIRONMENT')

logger.log_debug("Server Start")

if server_environment=="PRODUCTION":
    application = app
else:
    app.config["DEBUG"] = True
    app.run("0.0.0.0", "9201")
