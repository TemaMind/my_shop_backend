"""Определяет HTTP-маршрут /info для выдачи сводки по товарам."""

from flask import Flask, request, abort, Response
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from .config import Config
from .models import Product, Category
from .schemas import InfoParams
from .fetcher import start_background_fetch

app = Flask(__name__)
start_background_fetch()

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


@app.route("/info")
def info():
    """
    Обрабатывает GET /info с фильтрами.

    - category: имя категории
    - min_price, max_price: диапазон цен

    Возвращает текстовую сводку:
    всего товаров, средняя, мин/макс цены,
    список категорий, пример главного изображения.
    """
    # Валидация параметров
    try:
        params = InfoParams(**request.args)
    except Exception as e:
        abort(400, f"Invalid params: {e}")

    session = Session()
    try:
        # Базовый запрос с учётом фильтров
        query = session.query(Product).join(Category)
        if params.category:
            query = query.filter(Category.name == params.category)
        if params.min_price is not None:
            query = query.filter(Product.price >= params.min_price)
        if params.max_price is not None:
            query = query.filter(Product.price <= params.max_price)

        # Всего товаров
        total = query.count()

        # Средняя цена
        avg_price = query.with_entities(
            func.avg(Product.price)
        ).scalar() or 0.0

        # Мин и макс цена
        min_price, max_price = query.with_entities(
            func.min(Product.price),
            func.max(Product.price)
        ).one()
        if min_price is None or max_price is None:
            min_price = max_price = 0.0

        # Список категорий (distinct, отсортировано)
        categories = [
            c[0]
            for c in session.query(Category.name)
                            .order_by(Category.name)
                            .distinct()
        ]

        # Пример главного изображения
        image_record = (
            session.query(Product.image_url)
                   .filter_by(on_main=True)
                   .first()
        )
        image = image_record[0] if image_record and image_record[0] else "—"

        # Сборка текстового ответа
        lines = [
            f"Всего товаров: {total}",
            f"Средняя цена: {avg_price:.2f} руб.",
            f"Мин/макс цена: {min_price:.2f} — {max_price:.2f} руб.",
            f"Категории: {', '.join(categories) or '—'}",
            f"Пример главного изображения: {image}"
        ]
        return Response(
            "\n".join(lines),
            mimetype="text/plain; charset=utf-8"
        )

    finally:
        session.close()


if __name__ == "__main__":
    # Для локального запуска
    app.run(host="0.0.0.0", port=5555, threaded=True)
