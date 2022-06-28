import time

from app import initiate_app
from customLogger import setup_logger
from db import init_db

if __name__ == '__main__':
    """
    Entry point for the application.
    It sets up the database and the logger, and kicks off the app every 60 minutes.
    """
    init_db()
    setup_logger()
    # Executing the app every hour
    start_time = time.time()
    while True:
        initiate_app()
        time_Delay = 60 * 60
        time.sleep(time_Delay - ((time.time() - start_time) % time_Delay))
