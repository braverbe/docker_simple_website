# Используем образ Python
FROM python:3.11

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
WORKDIR /app
RUN pip install -r requirements.txt

# Запускаем веб-сервер
CMD ["python", "app.py"]