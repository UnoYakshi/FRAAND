# FRAAND

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


## License

This project uses the GPLv3 license. Please see the [LICENSE](LICENSE) for details.
