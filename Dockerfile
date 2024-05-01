FROM python:3.11-alpine3.17

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip -r /app/requirements.txt  # Install dependencies directly

COPY ./app /app

WORKDIR /app