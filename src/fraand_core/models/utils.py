"""
Utility functionality for FRAAND Core models...

- Adds support for alembic's migrations autogenerate feature.
"""

import importlib.util
import inspect
import logging
import os
from pathlib import Path

from src.fraand_core.constants import DOMAINS_PATH, IGNORED_ALEMBIC_SEARCH_DIR_NAMES, MODELS_DIRNAME, MODELS_FILENAME
from src.fraand_core.models.base import Base

logger = logging.getLogger('alembic.dynamic_import')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s  [%(name)s] %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

BIG_TAB = '\t' * 4


def import_domains_models() -> None:
    """
    Dynamically import all the `Base`-based models...

    The starting point is `src/fraand_core/domains/` directory. Since it goes recursively, sub-domains are fine as well.

    It's usually used:
      - either through `pdm run alembic revision --autogenerate -m "<revision name>"`
      - or upon FRAAND start up (in `scripts/entrypoint.sh`)
    """

    logger.info('')
    logger.info('▶▶▶▶ Start dynamical models importing...')

    for domains_root, domains_dirs, domains_files in os.walk(DOMAINS_PATH, topdown=True):

        # Filter un-needed folders to reduce `os.walk()` checks...
        domains_dirs[:] = list(filter(lambda x: x not in IGNORED_ALEMBIC_SEARCH_DIR_NAMES, domains_dirs))

        iter_msg = (
            '▶  Next iteration... \n'
            f'{BIG_TAB}Root: {domains_root}\n'
            f'{BIG_TAB}Dirs: {domains_dirs}\n'
            f'{BIG_TAB}Files: {domains_files}'
        )
        logger.info(iter_msg)

        # Check domain's `models.py` if any...
        if MODELS_FILENAME in domains_files:

            # Import the module...
            new_models_module_spec = importlib.util.spec_from_file_location(
                name=MODELS_DIRNAME,
                location=Path(domains_root) / MODELS_FILENAME,
            )
            new_models_module = importlib.util.module_from_spec(new_models_module_spec)
            new_models_module_spec.loader.exec_module(new_models_module)

            # Import the classes that are:
            # - inherited from Base model
            # - not Base model itself
            # - not an abstract model
            module_classes = []
            for _, cls in inspect.getmembers(new_models_module, inspect.isclass):
                if issubclass(cls, Base) and cls.__name__ != Base.__name__ and '__abstract__' not in cls.__dict__:
                    module_classes.append(cls)
            logger.info(f'\n{BIG_TAB}Imported classes: {module_classes}')

        # TODO: Check domain's `models/` directory if any...
        if MODELS_DIRNAME in domains_dirs:
            msg = 'Detected models/ folder yet there is no dynamic importing.'
            raise NotImplementedError(msg)

    logger.info('▶▶▶▶ Finished dynamical models importing.\n')
