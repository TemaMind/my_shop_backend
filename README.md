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

## Автор 
TemaMind