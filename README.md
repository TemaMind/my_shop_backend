# My Shop Backend

## Описание
Flask-приложение для периодической загрузки товаров из внешнего API и хранения их в PostgreSQL.

## Структура проекта
- `Dockerfile` — описание контейнера веб-сервиса.
- `docker-compose.yml` — оркестрация сервисов `web` и `db`.
- `requirements.txt` — список Python-зависимостей.
- `app/` — код приложения:
  - `config.py` — конфигурация из env.
  - `models.py` — SQLAlchemy-модели.
  - `fetcher.py` — фоновые задачи загрузки.
  - `schemas.py` — Pydantic-схемы для валидации.
  - `routes.py` — Flask-маршруты.
  - `logger.py` — настройка логирования.

## Требования
Docker и Docker Compose
Git

## Cтарт
1. Склонируйте репозиторий:

git clone https://github.com/TemaMind/my_shop_backend.git
cd my_shop_backend

2. Переименуйте .env.example в .env и при необходимости измените значения.

3. Поднимите сервисы:

docker compose up --build
Приложение будет доступно на http://127.0.0.1:5555.

## Логи

Логи появляются в консоли.

## Дополнение 

1. Маршрут /info

Возвращает текстовую сводку (Content-Type: text/plain; charset=utf-8):
Всего товаров (с учётом фильтров).
Средняя цена.
Минимальная и максимальная цена.
Список категорий.
Пример главного изображения.

2. Примеры запросов

2.1 curl "http://127.0.0.1:5555/info"

Фильтрация по категории и цене:

2.2 curl "http://127.0.0.1:5555/info?category=Одежда
2.3 curl "http://127.0.0.1:5555/info?min_price=50&max_price=100&min_price=10&max_price=100"




## Краткое описание решений
- **ORM (SQLAlchemy)**: модели `Category`/`Product` с явными ограничениями и каскадным удалением.
- **Фоновый поток**: `threading.Thread` для периодического обновления из API, настраивается через `FETCH_INTERVAL_SECONDS`.
- **Обработка данных**: функции ` _extract_items` и `_normalize_list_field` в `fetcher.py` для устойчивой работы с любым JSON.
- **Маршрут `/info`**: использует единый запрос `q`, применяет фильтры `category`, `min_price`, `max_price`, `name`, и собирает все метрики в одну таблицу.
- **Вывод**: текстовая ASCII-таблица удобна для чтения в терминале и браузере.

## Автор 
TemaMind