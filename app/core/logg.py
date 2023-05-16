import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    if not os.path.exists("logs/app.log"):
        with open("logs/app.log", "w") as f:
            pass

    log_level = (
        logging.DEBUG
    )  # Change this to the desired log level for your application
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    log_handler = TimedRotatingFileHandler("logs/app.log", when="midnight")
    log_handler.setLevel(log_level)
    log_handler.setFormatter(logging.Formatter(log_format))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(
        level=log_level, format=log_format, handlers=[log_handler, console_handler]
    )
