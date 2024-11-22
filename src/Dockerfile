FROM python:3.11

WORKDIR /src
COPY ./src /src

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "start.py"]