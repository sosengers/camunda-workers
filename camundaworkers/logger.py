import logging


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(threadName)s [%(levelname)s]: %(message)s"))
    logger.addHandler(ch)
    return logger

class Logger:
    logger = get_logger()

    def __init__(self):

