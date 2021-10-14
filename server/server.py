import time
import threading

import module_controller
import schedule

from app import api, app
import database_connection

api.add_resource(module_controller.GameController)
api.add_resource(module_controller.PlayerController)


def scheduler():
    schedule.every(10).seconds.do(module_controller.Data.store_games)
    while True:
        print("test")
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    database_connection.setup_database()
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.start()
    flask_thread = threading.Thread(target=app.run, args=("0.0.0.0", 5050))
    flask_thread.start()

    scheduler_thread.join()
    flask_thread.join()
