FROM python:3.9-slim-buster AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml pdm.lock fraand/ /app/

RUN python3 -m pip install --no-input --no-cache-dir --upgrade pip setuptools wheel
RUN python3 -m pip install --no-input --no-cache-dir --upgrade pdm

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable


FROM python:3.9-slim-buster

COPY --from=builder /app/__pypackages__/3.9/lib /app/pkgs
ENV PYTHONPATH=/app/pkgs

COPY fraand/ /app/fraand/

# set command/entrypoint, adapt to fit your needs
CMD export PYTHONPATH=$PYTHONPATH:/app/pkgs && python /app/fraand/manage.py makemigrations && python /app/fraand/manage.py migrate && python /app/fraand/manage.py runserver 0.0.0.0:8000
