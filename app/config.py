import os

class Config:
    # Строка подключения к БД
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv('DB_USER','shop')}:{os.getenv('DB_PASSWORD','shop_pass')}@"
        f"{os.getenv('DB_HOST','db')}:{os.getenv('DB_PORT','5432')}/{os.getenv('DB_NAME','shop_db')}"
    )

    # Интервал загрузки данных в секундах
    FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", 300))
