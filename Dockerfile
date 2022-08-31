FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN python3 -m pip install --no-input --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-input --no-cache-dir --upgrade pdm

RUN ["pdm", "install"]
