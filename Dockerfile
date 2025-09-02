FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Скопируем все файлы в контейнер
COPY . /app

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "bot.py"]