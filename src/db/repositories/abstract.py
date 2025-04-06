"""Repository file."""
import abc
from collections.abc import Sequence
from typing import Generic, TypeVar, Iterable

from sqlalchemy import delete, select, exists, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar('AbstractModel')


class Repository(Generic[AbstractModel]):
    """Repository abstract class."""

    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        """Get an ONE model from the database with PK.

        :param ident: Key which need to find entry in database
        :return:
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause, options=None) -> AbstractModel | None:
        """Get an ONE model from the database with whereclause.

        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None.
        """
        statement = select(self.type_model).where(whereclause)
        if options is not None:
            if isinstance(options, Iterable):
                statement = statement.options(*options)
            else:
                statement = statement.options(options)
        return await self.session.scalar(statement)

    async def get_many(
            self, whereclause=None, limit: int | None = 100, order_by=None
    ) -> Sequence[AbstractModel]:
        """Get many models from the database with whereclause.

        :param whereclause: Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause.

        Example:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
        """
        statement = select(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        if order_by is not None:
            statement = statement.order_by(order_by)
        if limit is not None:
            statement = statement.limit(limit)
        return (await self.session.scalars(statement)).all()

    async def get_pagination(self, offset: int, limit: int, order_by=None, whereclause=None, options=None) -> Sequence[AbstractModel]:
        stmt = select(self.type_model).offset(offset).limit(limit)
        if whereclause is not None:
            stmt = stmt.where(whereclause)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if options is not None:
            if isinstance(options, Iterable):
                stmt = stmt.options(*options)
            else:
                stmt = stmt.options(options)
        return (await self.session.scalars(stmt)).all()

    async def is_exists(self, whereclause=None) -> bool:
        stmt = select(exists().select_from(self.type_model))
        if whereclause is not None:
            stmt = stmt.where(whereclause)

        return await self.session.scalar(stmt)

    async def update(self, whereclause, values: dict):
        stmt = update(self.type_model).where(whereclause).values(**values)
        await self.session.execute(stmt)

    async def delete(self, whereclause=None) -> None:
        """Delete model from the database.

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        await self.session.execute(statement)

    async def count(self, whereclause=None) -> int | None:
        statement = select(func.count(self.type_model.id))
        if whereclause is not None:
            statement = statement.where(whereclause)
        return await self.session.scalar(statement)

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        """Add new entry of model to the database.

        :return: Nothing.
        """
        ...
