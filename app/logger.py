"""Настройка логгирования приложения с выводом в файл и консоль."""

import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    """
    Создаёт и настраивает логгер для приложения.

    Логи пишутся в файл `app.log` с ротацией и выводятся в консоль.
    """
    logger = logging.getLogger("shop")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Файловый хендлер с ротацией
    fh = RotatingFileHandler(
        "app.log",
        maxBytes=10**7,
        backupCount=3,
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Консольный хендлер
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


logger = setup_logger()
