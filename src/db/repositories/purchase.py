import uuid
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..enums import Lang
from ..models import Purchase, Item, CategoryLocalized, PositionLocalized


class PurchaseRepo(Repository[Purchase]):
    type_model: Purchase
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Purchase, session=session)

    async def new(self, *args, **kwargs) -> None:
        pass

    async def get_browse_category(self, category_id_fk: int) -> Sequence[Purchase]:
        stmt = select(Purchase).outerjoin(
            Purchase.item,
        ).where(
            Item.category_id_fk == category_id_fk
        )
        return (await self.session.scalars(stmt)).all()

    async def get_list_profile(self, user_id_fk: int, offset: int, limit: int):
        stmt = select(
            Purchase.id,
            Purchase.amount,
            Purchase.currency,
            Purchase.created_at,
            func.count(Item.id)
        ).where(
            Purchase.user_id_fk == user_id_fk
        ).outerjoin(
            Item, Item.purchase_id_fk == Purchase.id
        ).offset(
            offset
        ).limit(
            limit
        ).order_by(
            Purchase.created_at
        ).group_by(
            Purchase.id
        )
        return (await self.session.execute(stmt)).all()

    async def get_details(self, purchase_id: str, lang: Lang):
        stmt = select(
            func.array_agg(func.distinct(CategoryLocalized.name)).label("categories"),  # Собираем категории
            func.array_agg(func.distinct(PositionLocalized.name)).label("positions"),  # Собираем позиции
            Purchase.amount,
            Purchase.currency,
            Purchase.created_at,
            func.count(Item.id).label("item_count")
        ).outerjoin(
            Item, Item.purchase_id_fk == Purchase.id
        ).outerjoin(
            CategoryLocalized,
            (CategoryLocalized.category_id_fk == Item.category_id_fk) & (CategoryLocalized.lang == lang)
        ).outerjoin(
            PositionLocalized,
            (PositionLocalized.position_id_fk == Item.position_id_fk) & (PositionLocalized.lang == lang)
        ).where(
            Purchase.id == uuid.UUID(purchase_id)
        ).group_by(
            Purchase.id
        )

        return (await self.session.execute(stmt)).first()
