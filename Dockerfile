# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Скопируем файл зависимостей
COPY requirements.txt /app/

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем весь проект в контейнер
COPY . /app/

# # Соберем статику для Django
# RUN python manage.py collectstatic --noinput

# Указываем порт, который будет слушать Django
EXPOSE 8000

# Команда запуска Django-сервера с использованием ASGI
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "esp32cam_project.asgi:application"]