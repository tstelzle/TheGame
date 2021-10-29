import module_controller

from app import api, app
import database_connection
from apscheduler.schedulers.background import BackgroundScheduler

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)

database_connection.setup_database()

scheduler = BackgroundScheduler()
scheduler.add_job(func=module_controller.Data.store_games, trigger="interval", hours=12)
scheduler.start()

application = app
