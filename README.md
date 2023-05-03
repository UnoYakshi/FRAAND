`# FRAAND

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blue)](https://pdm.fming.dev)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)

Free Rent (it's called 'sharing') Application Among Neighbours [Decentrilized] platform.
Is a stuff sharing platform (aka social network).

## Development Prerequisites

1. Install [PDM](https://github.com/pdm-project/pdm) dependencies:
    - `pdm install --dev`
2. "Deploy" `pre-commit`:
    - `pre-commit install`
    - `pre-commit run`
3. Add `pdm-autoexport` so that dependencies changes would be automatically exported onto the `requirements/*.txt`.
   - `pdm plugin add pdm-autoexport`
4. Add [all the environment variables](docs/envars.md) in your `.env` (should be in the project's root).

## Planned Features

Check the [roadmap](docs/roadmap.md)!


## Used Instruments
To better understand the project, check a list of used instruments and libraries.
Some points also have commentaries about the reasoning behind a tool.
You will also find a tool's license in the brackets.

### Main Parts
- Python 3.11 —
- FastAPI (MIT) — REST API; roughly, Starlette + Pydantic
  - [FastAPI Users](https://fastapi-users.github.io) (MIT) — authentication and authorisation
  - [ORJSON](https://github.com/ijl/orjson) (Apache 2.0, MIT) — faster JSON processing
  - [Jinja2](https://jinja.palletsprojects.com/) (BSD-3-Clause) — for HTML templating, i.e., dead simple front-end
- uvicorn + gunicorn — server
- PostgreSQL — DB
- SQLAlchemy 1.4 + Alembic — ORM and migrations tool
  - kind of a world standard choice, useful to get into
  - SQLAlchemy Core can also be used to high-performance operations (e.g., to `bulk_update` 400K rows in a single transaction)
  - v. 1.4 was chosen [over v. 2.0] because SQLModel doesn't really support v. 2.0 yet (there is a [pull request](https://github.com/tiangolo/sqlmodel/pull/563))

### Code Quality
- [SQLModel](sqlmodel.tiangolo.com/) — intermediate layer between SQLAlchemy and Pydantic
  - allows to create Pydantic-ready DB models, hence, to reduce the code base for Pydantic schemes AND ORM models
- pre-commit + black + isort + mypy + flake8 — code quality

### CI/CD, extras
- Docker + docker compose (V2) — deployment
- pytest — integration and unit-testing


## License

This project uses the GPLv3 license. Please see the [LICENSE](LICENSE) for details.
