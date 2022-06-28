import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)


def setup_logger():
    """
    This function defines a logger that will make use of:
    - a handler that
        - backup logs at Midnight
        - Rotate the logs every 7 days
    - formatter
        - defines the format as timestamp, log level, and the message
    :return: None
    """
    global logger
    logger.handlers.clear()
    handler = TimedRotatingFileHandler(filename='storage/logs/app.log', when='midnight',
                                       interval=1, backupCount=7, encoding='utf-8',
                                       delay=False)
    formatter = Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
