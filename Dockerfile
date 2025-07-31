# Базовый образ
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /usr/src/app

# Копируем зависимости и ставим их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app ./app

# Открываем порт
EXPOSE 5555

# Команда запуска (используем Gunicorn с 4 воркерами)
CMD ["gunicorn", "--bind", "0.0.0.0:5555", "--preload", "app.routes:app", "--workers", "4"]
