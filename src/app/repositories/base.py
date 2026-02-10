import enum
import logging
from typing import Any, Generic, List, Optional, Tuple, TypeVar, Union

from sqlalchemy import ColumnElement, Select, asc, delete, desc, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

log = logging.getLogger(__name__)
T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[T],
    ):
        self.session = session
        self.model = model

    async def get_by_id(
        self,
        id: Any,
    ) -> T | None:
        return await self.session.get(self.model, id)

    async def add(self, instance: T) -> T:
        """
        Add a new object to the database.
        """
        log.info(f"Adding {self.model.__name__}: {instance}")
        try:
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(e)
            raise

    async def add_many(
        self,
        instances: List[T],
    ):
        """
        Add multiple objects to the database.
        """
        log.info(f"Adding multiple {self.model.__name__}. Count: {len(instances)}")
        try:
            self.session.add_all(instances)
            return instances
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(f"Error adding multiple {self.model.__name__}: {e}")
            raise

    async def get_all(  # noqa
        self,
        filters: Optional[dict] = None,
        order_by: Optional[List[Union[str, Tuple[str, str]]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Optional[T]]:
        """
        Get all objects with filtering, sorting and pagination.

        - order_by: list of strings or tuples for sorting, e.g.:
          ['name', ('age', 'desc')]
        - limit: maximum number of records
        - offset: offset (for pagination)
        """

        stmt: Select = select(self.model)

        try:
            log.info(f"Searching all {self.model.__name__} by filters: {filters}")
            if filters:
                expressions = []
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        continue  # пропускаем несуществующие поля

                    # Строковые поля → LIKE
                    if isinstance(value, str) and not isinstance(value, enum.Enum):
                        expressions.append(column.ilike(f"%{value}%"))
                    else:
                        # Прочие поля → обычное сравнение
                        expressions.append(column == value)

                if expressions:
                    stmt = stmt.where(*expressions)

            if order_by:
                ordering = []
                for item in order_by:
                    if isinstance(item, str):
                        # сортировка по возрастанию
                        ordering.append(asc(getattr(self.model, item)))
                    elif isinstance(item, tuple) and len(item) == 2:  # noqa
                        col_name, direction = item
                        col = getattr(self.model, col_name)
                        if direction.lower() == "desc":
                            ordering.append(desc(col))
                        else:
                            ordering.append(asc(col))
                stmt = stmt.order_by(*ordering)

            if limit is not None:
                stmt = stmt.limit(limit)

            if offset is not None:
                stmt = stmt.offset(offset)

            result = await self.session.execute(stmt)
            records = result.unique().scalars().all()
            log.info(f"Found {len(records)} {self.model.__name__}.")
            return records
        except SQLAlchemyError as e:
            log.error(
                f"Error searching all {self.model.__name__} by filters {filters}: {e}"
            )
            raise

    async def update_by_id(
        self,
        id_: Any,
        values: dict,
    ) -> Optional[T]:
        """
        Update an object by id.
        """
        log.info(f"Updating {self.model.__name__} by id: {id_}")
        if not values:
            return await self.get_by_id(id_)

        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**values)
            .execution_options(synchronize_session="fetch")
            .returning(self.model)
        )

        try:
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(e)
            raise

    async def delete_by_id(self, id_: Any) -> bool:
        """
        Delete an object by id.
        """
        log.info(f"Deleting {self.model.__name__} by id: {id_}")
        stmt = delete(self.model).where(self.model.id == id_)
        try:
            result = await self.session.execute(stmt)
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            log.error(e)
            raise

    async def find_one(
        self,
        filters: List[ColumnElement],
        order_by: Optional[List[Union[str, Tuple[str, str]]]] = None,
    ) -> Optional[T]:
        """
        Find one object by filters.
        """
        log.info(f"Finding one {self.model.__name__} by filters: {filters}")
        stmt = select(self.model)

        for condition in filters:
            stmt = stmt.where(condition)

        if order_by:
            ordering = []
            for item in order_by:
                if isinstance(item, str):
                    ordering.append(asc(getattr(self.model, item)))
                else:
                    col, direction = item
                    column = getattr(self.model, col)
                    ordering.append(
                        desc(column) if direction.lower() == "desc" else asc(column)
                    )
            stmt = stmt.order_by(*ordering)

        result = await self.session.execute(stmt)
        return result.scalars().first()
