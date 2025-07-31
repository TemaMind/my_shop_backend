import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("shop")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    fh = RotatingFileHandler("app.log", maxBytes=10**7, backupCount=3)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger

logger = setup_logger()
