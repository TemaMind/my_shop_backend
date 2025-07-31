from flask import Flask, request, abort, Response
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from .config import Config
from .models import Product, Category
from .schemas import InfoParams
from .fetcher import start_background_fetch
from .logger import logger

app = Flask(__name__)
start_background_fetch()

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)

@app.route("/info")
def info():
    # Валидация параметров
    try:
        params = InfoParams(**request.args)
    except Exception as e:
        abort(400, f"Invalid params: {e}")

    session = Session()
    try:
        # Базовый запрос с учётом фильтров
        q = session.query(Product).join(Category)
        if params.category:
            q = q.filter(Category.name == params.category)
        if params.min_price is not None:
            q = q.filter(Product.price >= params.min_price)
        if params.max_price is not None:
            q = q.filter(Product.price <= params.max_price)

        # Всего товаров
        total = q.count()

        # Средняя цена
        avg_price = q.with_entities(func.avg(Product.price)).scalar() or 0.0

        # Мин/макс цена
        min_price, max_price = q.with_entities(
            func.min(Product.price),
            func.max(Product.price)
        ).one()
        # Если нет товаров, убираем None
        if min_price is None or max_price is None:
            min_price = max_price = 0.0

        # Список категорий
        cats = [c[0] for c in session.query(Category.name)
                .order_by(Category.name)
                .distinct()]

        # Пример главного изображения
        img_rec = session.query(Product.image_url)\
                         .filter_by(on_main=True)\
                         .first()
        img = img_rec[0] if img_rec and img_rec[0] else "—"

        # Собираем ответ
        lines = [
            f"Всего товаров: {total}",
            f"Средняя цена: {avg_price:.2f} руб.",
            f"Мин/макс цена: {min_price:.2f} — {max_price:.2f} руб.",
            f"Категории: {', '.join(cats) or '—'}",
            f"Пример главного изображения: {img}"
        ]
        return Response("\n".join(lines), mimetype="text/plain; charset=utf-8")
    finally:
        session.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, threaded=True)

