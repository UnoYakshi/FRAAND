"""
Provides the access to global constants across the core project.

Such as:
- absolute paths
- folders names
"""

from pathlib import Path

MAIN_APP_DIR = Path(__file__).parent.absolute()
SRC_DIR = Path(MAIN_APP_DIR).parent.absolute()

DOMAINS_PATH = MAIN_APP_DIR / 'domains'

IGNORED_ALEMBIC_SEARCH_DIR_NAMES = ['__pycache__', 'schemas']
MODELS_DIRNAME = 'models'
MODELS_FILENAME = 'models.py'

TEMPLATES_DIR_NAME = 'templates'
TEMPLATES_ABS_FILE_PATH = Path(MAIN_APP_DIR) / TEMPLATES_DIR_NAME

STATIC_DIR_NAME = 'static'
STATIC_ABS_FILE_PATH = Path(MAIN_APP_DIR) / STATIC_DIR_NAME
