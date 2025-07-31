import threading
import time
import json
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from .config import Config
from .models import Base, Category, Product
from .logger import logger

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)

def wait_for_db():
    """Ждём, пока СУБД не ответит на connect()."""
    while True:
        try:
            conn = engine.connect()
            conn.close()
            logger.info("Database is available")
            break
        except OperationalError:
            logger.info("Database unavailable, retrying in 1s…")
            time.sleep(1)

def init_db():
    Base.metadata.create_all(engine)
    logger.info("Database schema created")

def _extract_items(raw_json):
    """
    Извлекает список продуктов из произвольного JSON:
     - если это list — возвращаем его,
     - если dict с ключом 'products' или 'items' — возвращаем raw['products'] или raw['items'],
     - иначе находим все списки в значениях dict и конкатенируем их,
     - иначе — пустой список.
    """
    if isinstance(raw_json, list):
        return raw_json
    if isinstance(raw_json, dict):
        # явно заданные ключи
        for key in ("products", "items", "data"):
            if key in raw_json and isinstance(raw_json[key], list):
                return raw_json[key]
        # все списки в значениях
        lists = [v for v in raw_json.values() if isinstance(v, list)]
        if lists:
            result = []
            for lst in lists:
                result.extend(lst)
            return result
    return []

def _normalize_list_field(raw, key_name=None):
    """
    Берёт поле, которое может быть:
      - list
      - dict
      - JSON-строка
      - простой текст
    Всегда возвращает list. Если key_name задан,
    то для "сырого" значения возвращает dict {key_name: raw}.
    """
    if raw is None:
        return []
    # JSON-строка
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            return _normalize_list_field(parsed, key_name)
        except (ValueError, TypeError):
            return [{key_name: raw}] if key_name else [raw]
    # чистый список
    if isinstance(raw, list):
        return raw
    # один словарь
    if isinstance(raw, dict):
        return [raw]
    # всё остальное — приведём к строке
    return [{key_name: str(raw)}] if key_name else [str(raw)]

def fetch_and_update():
    session = Session()
    try:
        # 1) Вытаскиваем два набора «сырого» JSON
        resp1 = requests.get("https://bot-igor.ru/api/products?on_main=true", timeout=10)
        resp1.raise_for_status()
        resp2 = requests.get("https://bot-igor.ru/api/products?on_main=false", timeout=10)
        resp2.raise_for_status()

        # 2) Извлекаем списки продуктов
        items_true  = _extract_items(resp1.json())
        items_false = _extract_items(resp2.json())
        items = items_true + items_false

        # 3) Полная очистка старых данных
        session.query(Product).delete()
        session.query(Category).delete()
        session.commit()

        # 4) Проходим по каждому «item» — ожидаем dict с ключами Product_… и вспомогательными
        for item in items:
            if not isinstance(item, dict):
                logger.warning("Skipping non-dict item: %r", item)
                continue

            # --- CATEGORY ---
            cats = _normalize_list_field(item.get("categories"), key_name="Category_Name")
            cat_name = cats[0].get("Category_Name", "").strip() if cats else ""
            if not cat_name:
                logger.warning("Skipping item without category: %r", item)
                continue

            # --- PRICE ---
            params = _normalize_list_field(item.get("parameters"), key_name="price")
            try:
                price = float(params[0].get("price", 0))
            except Exception:
                price = 0.0
                logger.warning("Invalid price %r for item %r", params, item)

            # --- IMAGE ---
            imgs = _normalize_list_field(item.get("images"), key_name="Image_URL")
            image_url = imgs[0].get("Image_URL", "").strip() if imgs else ""

            # --- INSERT ---
            # Категория
            cat = session.query(Category).filter_by(name=cat_name).first()
            if not cat:
                cat = Category(name=cat_name)
                session.add(cat)
                session.flush()

            # Продукт
            prod = Product(
                id       = item.get("Product_ID"),
                name     = item.get("Product_Name", "").strip(),
                price    = price,
                image_url= image_url,
                on_main  = bool(item.get("OnMain", False)),
                category = cat
            )
            session.add(prod)

        session.commit()
        logger.info("Fetched and updated %d products", len(items))

    except Exception:
        logger.exception("Error fetching data")
        session.rollback()
    finally:
        session.close()

def start_background_fetch():
    logger.info("Waiting for database…")
    wait_for_db()
    init_db()

    def worker():
        while True:
            fetch_and_update()
            time.sleep(Config.FETCH_INTERVAL_SECONDS)

    t = threading.Thread(target=worker, daemon=True, name="fetcher")
    t.start()
    logger.info("Background fetch thread started")
