from collections.abc import Sequence

from aiogram.enums import ContentType
from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .abstract import Repository
from ..enums import Lang
from ..models import Item, Category, CategoryLocalized, Position, PositionLocalized


class ItemRepo(Repository[Item]):
    type_model: Item
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Item, session=session)

    async def new(
            self,
            category_id_fk: int,
            position_id_fk: int,
            content: str,
            content_type: ContentType | None = None
    ) -> Item:
        return await self.session.merge(
            Item(
                category_id_fk=category_id_fk,
                position_id_fk=position_id_fk,
                content=content,
                content_type=content_type
            )
        )

    async def clear(self, position_id_fk: int):
        items: Sequence[Item] = await self.get_many(
            Item.position_id_fk == position_id_fk,
            limit=9999,
            order_by=Item.id
        )
        for item in items:
            if item.purchase_id_fk is not None:
                item.position_id_fk = None
                item.category_id_fk = None
            else:
                await self.session.delete(item)

    async def get_with_category_position(self, item_id: int, lang: Lang) -> Item | None:
        stmt = select(
            Item
        ).options(
            joinedload(Item.category).selectinload(Category.category_localized.and_(CategoryLocalized.lang == lang)),
            joinedload(Item.position).selectinload(Position.position_localized.and_(PositionLocalized.lang == lang)),
        ).where(Item.id == item_id)
        return await self.session.scalar(stmt)