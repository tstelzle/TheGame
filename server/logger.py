import logging


def create_logger(logfile: str):
    logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.DEBUG)


def log_debug(message: str):
    logging.debug(message)


def log_error(message: str):
    logging.error(message)