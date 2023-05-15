# FRAAND

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blue)](https://pdm.fming.dev)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)

Free Rent (it's called 'sharing') Application Among Neighbours [Decentralized] platform.
Is a stuff sharing platform (aka social network).


## Development Prerequisites

1. Install [PDM](https://github.com/pdm-project/pdm).
2. Install PDM dependencies, `pdm install --dev`
3. "Deploy" [pre-commit](https://pre-commit.com/):
    - `pre-commit install`
    - `pre-commit run`
4. Add `pdm-autoexport` so that dependencies changes would be automatically exported onto the `requirements/*.txt`.
   - `pdm plugin add pdm-autoexport`
5. Add [all the environment variables](docs/envars.md) in your `.env` (should be in the project's root).


## Planned Features

Check the [roadmap](docs/roadmap.md)!


## Used Instruments
To better understand the project, check a list of used instruments and libraries.
Some points also have commentaries about the reasoning behind a tool.
You will also find a tool's license in the brackets.

### Main Parts
- Python 3.11 ([PSF](https://docs.python.org/3/license.html#psf-license)) — cool and modern version
- FastAPI (MIT) — REST API; roughly, Starlette + Pydantic
  - [FastAPI Users](https://fastapi-users.github.io) (MIT) — authentication and authorisation
  - [ORJSON](https://github.com/ijl/orjson) (Apache 2.0, MIT) — faster JSON processing
  - [Jinja2](https://jinja.palletsprojects.com/) (BSD 3-Clause) — for HTML templating, i.e., dead simple front-end
- uvicorn (BSD 3-Clause) + gunicorn (MIT) — ASGI + WSGI HTTP servers
- PostgreSQL ([PostgreSQL](https://opensource.org/license/postgresql/)) — DB
- SQLAlchemy 1.4 (MIT) + Alembic (MIT) — ORM and migrations tool
  - kind of a world standard choice, useful to get into
  - SQLAlchemy Core can also be used to high-performance operations (e.g., to `bulk_update` 400K rows in a single transaction)
  - v. 1.4 was chosen [over v. 2.0] because SQLModel doesn't really support v. 2.0 yet (there is a [pull request](https://github.com/tiangolo/sqlmodel/pull/563))

### Code Quality
- pre-commit (MIT) — git hooks to disallow commits with low code quality
- black (MIT) — automatic code formatter
- isort (MIT) — imports sorting utility
- mypy (MIT) — static type checker
- Ruff (MIT) — a vast code quality tool, Flake8 (and its plugins) super-performant alternative

### CI/CD, management, extras
- PDM — package manager, sophisticated enough to fulfil the most (if not all) our needs
- Docker + docker compose (V2) — deployment
- pytest — integration and unit-testing


## File Structure
You've probably already guessed what's the project about and how it can be structured.
Yet, to get into the project easier, let's go through the most important parts...

### Root
- [pyproject.toml](pyproject.toml) is the starting point of FRAAND.
It's where all the project's metadata is stored, according to [PEP-621](https://peps.python.org/pep-0621/).
- Most of the configuration files are also in the root. Such as:
  - [.dockerignore](.dockerignore) — what [Dockerfile](Dockerfile) should ignore.
  - [.pre-commit-config.yaml](.pre-commit-config.yaml) — [pre-commit] hooks config.
  - [mypy.ini](mypy.ini) — typing checker tool config.
  - [alembic.ini](alembic.ini) — DB migrations config.
- [Dockerfile](Dockerfile) — Docker image build instructions.
- [docker-compose.dev.yml](docker-compose.dev.yml) — is responsible for local development deployment.
- `docs/` — self-explanatory, documentation.
- `alembic/` — Alembic migrations directory.
  - `versions/` — actual migration files.
- `requirements/` — here you can find dead simple `.txt` requirements for different environments (dev, stage, production).
- `scripts/` — a great place to put a standalone script
if you want to execute it outside the FRAAND Core logic (and it's too small for a separate microservice).

### Source Code
- `src/fraand_core/` — all the actual FRAAND platform's code is located here.
  - `domains/` — all the logical parts of the platform. Each domain might have:
    - `dependencies.py/` — FastAPI `Depends()` methods.
    - `models/` — this domain's ORM models.
    - `schemas/` — Pydantic schemas for endpoints/models.
    - `exceptions/` — custom domain's exceptions.
    - `constants/` — a place to put your static data such as constants or function maps.
    - `serivce/` — all the business logic functionality.
    - `router/` — [WIP] domain's endpoints composed into an `APIRouter`.
    - `utils/` — [WIP] any utility that doesn't necessary a part of the domain but is used only here.
  - `models/` — ORM models used by some (2..N) domains.
  - `crud/` — [WIP] a base class for ORM CRUD-managers.
  - `routers/` — [WIP] a single point to have all the
  - `utils/` — general utility functionality.

(*) — [WIP] directories are likely to be reworked soon enough.


## License

This project uses the GPLv3 license. Please see the [LICENSE](LICENSE) for details.
