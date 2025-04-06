from typing import Sequence, Any

from sqlalchemy import select, func, Row, RowMapping, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .abstract import Repository
from ..enums import Lang
from ..models import Category, CategoryLocalized, Position, Item


class CategoryRepo(Repository[Category]):
    type_model: Category
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Category, session=session)

    async def new(self) -> Category:
        return await self.session.merge(
            Category()
        )

    async def create_category(self, category_ru_name: str, category_en_name: str | None = None) -> Category:
        category = Category()
        category.category_localized.append(
            CategoryLocalized(
                name=category_ru_name,
                lang=Lang.RU
            )
        )
        category.category_localized.append(
            CategoryLocalized(
                name=category_en_name,
                lang=Lang.EN
            )
        )
        return await self.session.merge(category)

    async def get_shopping(
            self,
            lang: Lang,
            offset: int,
            limit: int,
            category_without_items: bool
    ):
        stmt = (
            select(Category.id, CategoryLocalized.name)
            .join(CategoryLocalized,
                  (Category.id == CategoryLocalized.category_id_fk) & (CategoryLocalized.lang == lang))
            .offset(offset)
            .limit(limit)
            .order_by(Category.id)
        )
        if not category_without_items:
            stmt = stmt.where(
                exists().where((Item.category_id_fk == Category.id) & (Item.purchase_id_fk.is_(None)))
            )
        return (await self.session.execute(stmt)).all()

    async def get_count_shopping(self, category_without_items: bool) -> int:
        stmt = select(func.count(Category.id))
        if not category_without_items:
            stmt = stmt.where(
                exists().where((Item.category_id_fk == Category.id) & (Item.purchase_id_fk.is_(None))))
        return await self.session.scalar(stmt)

    async def get_browse_category(self, category_id: int, lang: Lang) -> Sequence[
        Row[Any] | RowMapping | Any]:
        stmt = select(Category, func.count(Position.id), func.count(Item.id)).options(
            selectinload(Category.category_localized.and_(CategoryLocalized.lang == lang))).outerjoin(
            Category.position
        ).outerjoin(
            Category.item
        ).where(Category.id == category_id).group_by(Category.id)
        return (await self.session.execute(stmt)).all()

    async def get_many_localized(self, lang: Lang) -> Sequence[Category]:
        stmt = select(Category).options(selectinload(
            Category.category_localized.and_(CategoryLocalized.lang == lang)
        ))
        return (await self.session.scalars(stmt)).all()

    async def get_with_locales(self, category_id: int) -> Category | None:
        stmt = select(Category).options(selectinload(Category.category_localized)).where(Category.id == category_id)
        return await self.session.scalar(stmt)
