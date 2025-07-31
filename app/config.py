"""
Модуль конфигурации.

Загружает настройки из переменных окружения с разумными
значениями по умолчанию.
"""

import os


class Config:
    """Класс базовой конфигурации приложения."""

    # URI подключения SQLAlchemy.
    # Формат: postgresql://user:password@host:port/dbname
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://{user}:{password}@{host}:{port}/{db}".format(
            user=os.getenv("DB_USER", "shop"),
            password=os.getenv("DB_PASSWORD", "shop_pass"),
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", "5432"),
            db=os.getenv("DB_NAME", "shop_db"),
        ),
    )

    #: Интервал между фоновыми загрузками данных (в секундах).
    FETCH_INTERVAL_SECONDS = int(
        os.getenv("FETCH_INTERVAL_SECONDS", "300")
    )
