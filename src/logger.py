import logging

logger = logging.getLogger("OCD_MISP")

LOG_FORMAT = "%(name)s:%(levelname)-4s %(message)s"


def configure_logging(loglevel: int):
    handler = logging.StreamHandler()

    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loglevel)
