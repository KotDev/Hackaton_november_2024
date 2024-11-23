FROM python:3.11-slim

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

