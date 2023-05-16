"""Custom exceptions for CRUD managers..."""

from src.fraand_core.crud.annotations import ModelType


class NotImplementedUniqueKeysError(NotImplementedError):
    """Should be raised in cases where unique keys (in models) are expected. Initially was made for CRUDBase..."""

    def __init__(self, model: type[ModelType]) -> None:
        """Error-message based on the provided model..."""
        super().__init__(f'The model [{model}] must implement the `unique_keys` property!')
