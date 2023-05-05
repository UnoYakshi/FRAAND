"""
Defines the base manager with generic logic for CRUD-operations.

Every model should inherit this logic and enrich/override it if needed.
Notice that CRUD-functions DO NOT validate the given input,
therefore you should validate the arguments before passing them into the CRUD-functions.
"""


from typing import Any, Generic, Type, Union

from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.fraand_core.config import settings
from src.fraand_core.crud.annotations import CreateSchemaType, ModelType, UpdateSchemaType
from src.fraand_core.crud.exceptions import NotImplementedUniqueKeysError


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """General CRUD manager for ORM models..."""

    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD-manager constructor...

        :param model: The type of on ORM model to work with...
        """
        self.model = model

    async def create(
        self,
        session: AsyncSession,
        in_obj: CreateSchemaType,
        **attrs: Any,
    ) -> ModelType:
        """
        Tso (and adds it to the DB)...

        :param session: Async SQLAlchemy session, usually got from a dependency...
        :param in_obj: Dict-like data for a new object based Pydantic update schema...
        :param attrs: What is that for?.. Some extra parameters?..
        """

        in_obj_data = jsonable_encoder(in_obj)
        attrs_data = jsonable_encoder(attrs)
        db_obj = self.model(**in_obj_data, **attrs_data)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def read(self, session: AsyncSession, **attrs: Any) -> ModelType | None:
        """
        Getter, returns [the first] found scalar...

        :param session: Async SQLAlchemy session, usually got from a dependency...
        :param attrs: Dict-like attributes for `filter_by()`...

        :return: [The first] found scalar satisfying the filter attributes if found, otherwise None...
        """

        statement = select(self.model).filter_by(**attrs)
        result = await session.execute(statement=statement)
        return result.scalars().first()

    async def read_or_404(self, session: AsyncSession, **attrs: Any) -> ModelType:
        """
        Just as `self.read(..)` but will raise 404 if such object doesn't exist in the DB...

        :param session: Async SQLAlchemy session, usually got from a dependency...
        :param attrs: Used as in `self.read()`...

        :return: Model row (object, not scalar), otherwise raises 404...
        :raises HTTPException: If the row-object with provided attributes wasn't found...
        """

        db_obj = await self.read(session=session, **attrs)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__tablename__.capitalize()} not found',
            )
        return db_obj

    async def read_many(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = settings.PAGE_SIZE,
        **attrs: Any,
    ) -> list[ModelType]:
        """Paginated getter, the results are scalar. WARNING: it's not a `bulk_*()` operation..."""

        statement = select(self.model).filter_by(**attrs).offset(skip).limit(min(limit, settings.PAGE_SIZE))
        result = await session.execute(statement=statement)
        return result.scalars().all()

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        in_obj: Union[UpdateSchemaType, dict[str, Any]],
    ) -> ModelType:
        """
        Updates the given object [of this ORM model] with provided data (via Pydantic schema's interface)...

        :param session: Async SQLAlchemy session, usually got from a dependency...
        :param db_obj: The object to update...
        :param in_obj: Data to update the provided object with...
        """

        obj_data = jsonable_encoder(db_obj)
        update_data = in_obj if isinstance(in_obj, dict) else in_obj.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def delete(self, session: AsyncSession, db_obj: ModelType) -> ModelType | None:
        """
        Deletes the given object [of this ORM model]...

        :param session: Async SQLAlchemy session, usually got from a dependency...
        :param db_obj: The actual DB object to delete...
        """

        await session.delete(db_obj)
        await session.commit()
        return db_obj

    def parse_integrity_error(self, error: IntegrityError) -> dict[str, Any]:
        """
        Parses PostgreSQL `IntegrityError`...

        :return: FastAPI log message (with `loc` and `msg`) where the error took place...

        :raises NotImplementedError: if there are no unique_keys in the ORM model...
        :raises IntegrityError: if it's not Postgres' `UniqueViolationError`
        """

        if not self.model.unique_keys:
            raise NotImplementedUniqueKeysError(self.model)

        # TODO: Ensure it works just as same... if error.orig.pgcode != '23505:  # UniqueViolationError...
        if error.orig != UniqueViolationError:
            error_args_str = ''.join(error.orig.args)
            for key in self.model.unique_keys:
                if error_args_str.find(key) != -1:
                    return {
                        'loc': ['body', key],
                        'msg': 'value already exists',
                    }

        raise error
