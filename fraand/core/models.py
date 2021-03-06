"""Base abstract models that all project models should inherit from."""

# WARNING: you cannot define concrete models in this module.
# Only abstract models, such as MyBaseModel below, can be defined here.
# The `core` "app" cannot be added to `INSTALLED_APPS` setting, and therefore
# any non-abstract (known as "concrete") models will not be detected here.

import uuid

from django.db import models

from fraand.core.managers import MyBaseQuerySet


class MyBaseModel(models.Model):
    """Base abstract model for all models used throughout the project."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = MyBaseQuerySet.as_manager()

    # Basic time tracking for all models (for sorting)...
    created_at = models.DateTimeField("created", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("updated", auto_now=True, db_index=True)

    class Meta:
        abstract = True
