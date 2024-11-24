# Используем образ Python, чтобы уже иметь все инструменты для работы с Python
FROM python:3.11-slim

# Обновляем и устанавливаем нужные пакеты для локалей
RUN apt-get update && apt-get install -y locales \
    && locale-gen ru_RU.UTF-8 \
    && dpkg-reconfigure locales

# Устанавливаем переменные окружения для локалей
ENV LANG=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8
ENV LC_TIME=ru_RU.UTF-8

WORKDIR /src

# Обновить pip и инструменты сборки
RUN pip install --upgrade pip setuptools wheel

# Копировать код
COPY ./src /src

# Установить зависимости
RUN pip install -r requirements.txt

# Установить Playwright
RUN playwright install

EXPOSE 8000

CMD ["python", "start.py"]
