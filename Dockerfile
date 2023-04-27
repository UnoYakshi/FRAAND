FROM python:3.10-slim-buster AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml pdm.lock /app/

RUN python3 -m pip install --no-input --no-cache-dir --upgrade pip setuptools wheel
RUN python3 -m pip install --no-input --no-cache-dir --upgrade pdm

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable
RUN python -V
RUN ls /app
RUN ls /app/__pypackages__

FROM python:3.10-slim-buster

COPY --from=builder /app/__pypackages__/3.10/lib /app/__pypackages__/3.9/lib/
COPY fraand/ /app/fraand/

#ENV PYTHONPATH "${PYTHONPATH}:/app/__pypackages__:/app/pkgs:/app/pkgs/3.10/lib"
#ENV PYTHONPATH=$PYTHONPATH:/app/pkgs/

# set command/entrypoint, adapt to fit your needs
CMD python /app/fraand/manage.py makemigrations && python /app/fraand/manage.py migrate && python /app/fraand/manage.py runserver 0.0.0.0:8000
#CMD export PYTHONPATH=$PYTHONPATH:/app/__pypackages__ && pwd && ls /app/__pypackages__/3.10/lib && python /app/fraand/manage.py makemigrations && python /app/fraand/manage.py migrate && python /app/fraand/manage.py runserver 0.0.0.0:8000
#CMD pdm run export PYTHONPATH=$PYTHONPATH:/app/__pypackages__ && /app/fraand/manage.py makemigrations && pdm run /app/fraand/manage.py migrate && pdm run /app/fraand/manage.py runserver 0.0.0.0:8000
#CMD ls /app && python -m pdm run /app/fraand/manage.py runserver 0.0.0.0:8000
#CMD ls /app && echo "--" && python -V && echo "--" && ls /app/pkgs && echo $PYTHONPATH && python /app/fraand/manage.py runserver 0.0.0.0:8000
#CMD ls /app/ && echo "--" && python -V && echo "--" && echo $PYTHONPATH
#CMD ["python3", "/app/fraand/manage.py", "runserver", "0.0.0.0:8000"]
