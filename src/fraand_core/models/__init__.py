"""
Adds support for alembic's migrations autogenerate feature...

Dynamically adds all the models in src/fraand_core/domains/. Since it goes recursively, sub-domains are fine...
"""

from src.fraand_core.models.base import Base
