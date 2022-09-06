FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER fraand

WORKDIR /app
COPY . /app

RUN chown -R 755 fraand /app

RUN python3 -m pip install --no-input --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-input --no-cache-dir --upgrade pdm

RUN pdm config python.use_venv false
RUN ["pdm", "install"]
