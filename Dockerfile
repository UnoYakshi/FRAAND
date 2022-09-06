FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN useradd -m -r fraand && \
    chown -R 755 fraand /app

RUN python3 -m pip install --no-input --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-input --no-cache-dir --upgrade pdm

USER fraand

RUN pdm config python.use_venv false
RUN ["pdm", "install"]
