# Используем образ PostgreSQL
FROM postgres:latest

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get -y install vim

# Копируем конфигурационный файл
COPY postgresql.conf /etc/postgresql/postgresql.conf

# Копируем скрипт инициализации базы данных
COPY init.sql /docker-entrypoint-initdb.d/