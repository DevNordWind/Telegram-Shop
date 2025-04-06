from decimal import Decimal
from typing import Sequence

from aiogram.enums import ContentType
from sqlalchemy import select, update, exists, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .abstract import Repository
from ..enums import Lang, Currency
from ..models import Position, PositionLocalized, Category, CategoryLocalized, PositionPrice, Item


class PositionRepo(Repository[Position]):
    type_model: Position
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Position, session=session)

    async def new(self):
        pass

    async def create_position(self,
                              category_id_fk: int,
                              ru_name: str,
                              en_name: str,
                              ru_price: Decimal,
                              en_price: Decimal,
                              ru_description: str,
                              en_description: str,
                              file_path: str | None = None,
                              file_id: str | None = None,
                              content_type: ContentType | None = None
                              ):
        position = Position(
            category_id_fk=category_id_fk,
            file_path=file_path,
            file_id=file_id,
            content_type=content_type
        )
        position.position_localized.append(PositionLocalized(
            name=ru_name,
            description=ru_description,
            lang=Lang.RU,
        ))
        position.position_localized.append(PositionLocalized(
            name=en_name,
            description=en_description,
            lang=Lang.EN,
        ))

        position.position_price.append(PositionPrice(
            price=ru_price,
            currency=Currency.RUB,
        ))
        position.position_price.append(PositionPrice(
            price=en_price,
            currency=Currency.USD,
        ))
        return await self.session.merge(
            position
        )

    async def get_localized_category(self, position_id: int, lang: Lang, currency: Currency) -> Position | None:
        stmt = (select(
            Position
        ).options(
            selectinload(Position.position_localized.and_(PositionLocalized.lang == lang)),
            selectinload(Position.position_price.and_(PositionPrice.currency == currency)),
            selectinload(Position.item),
            selectinload(Position.category).selectinload(
                Category.category_localized.and_(CategoryLocalized.lang == lang))
        ).where(
            Position.id == position_id)
        )
        return await self.session.scalar(stmt)

    async def get_many_localized_category(self, category_id_fk: int, lang: Lang, currency: Currency) -> Sequence[
        Position]:
        stmt = (select(
            Position
        ).options(
            selectinload(Position.position_localized.and_(PositionLocalized.lang == lang)),
            selectinload(Position.position_price.and_(PositionPrice.currency == currency)),
            selectinload(Position.item.and_(Item.purchase_id_fk == None)),
            selectinload(Position.category).selectinload(
                Category.category_localized.and_(CategoryLocalized.lang == lang))
        ).where(
            Position.category_id_fk == category_id_fk)
        )
        return (await self.session.scalars(stmt)).all()

    async def update_names(self, position_id: int, name_ru: str, name_en: str) -> None:
        stmt = update(
            PositionLocalized
        ).where(PositionLocalized.position_id_fk == position_id, PositionLocalized.lang == Lang.RU).values(
            {
                'name': name_ru
            }
        )
        second_stmt = update(
            PositionLocalized
        ).where(PositionLocalized.position_id_fk == position_id, PositionLocalized.lang == Lang.EN).values(
            {
                'name': name_en
            }
        )
        await self.session.execute(stmt)
        await self.session.execute(second_stmt)

    async def update_prices(self, position_id: int, price_rub: Decimal, price_usd: Decimal) -> None:
        update_rub = update(
            PositionPrice
        ).where(
            PositionPrice.position_id_fk == position_id, PositionPrice.currency == Currency.RUB
        ).values(
            {
                'price': price_rub
            }
        )
        update_usd = update(
            PositionPrice
        ).where(
            PositionPrice.position_id_fk == position_id, PositionPrice.currency == Currency.USD
        ).values(
            {
                'price': price_usd
            }
        )
        await self.session.execute(update_rub)
        await self.session.execute(update_usd)

    async def update_description(self, position_id: int, ru_description: str, en_description: str) -> None:
        update_ru = update(
            PositionLocalized
        ).where(
            PositionLocalized.position_id_fk == position_id, PositionLocalized.lang == Lang.RU
        ).values(
            {
                'description': ru_description
            }
        )
        update_en = update(
            PositionLocalized
        ).where(
            PositionLocalized.position_id_fk == position_id, PositionLocalized.lang == Lang.EN
        ).values(
            {
                'description': en_description
            }
        )
        await self.session.execute(update_ru)
        await self.session.execute(update_en)

    async def get_shopping(
            self,
            category_id_fk: int,
            lang: Lang,
            currency: Currency,
            position_without_items: bool,
            offset: int,
            limit: int
    ):
        stmt = (
            select(Position.id, PositionLocalized.name, PositionPrice.price)
            .join(PositionLocalized,
                  (Position.id == PositionLocalized.position_id_fk) & (PositionLocalized.lang == lang)
                  )
            .join(
                PositionPrice,
                (Position.id == PositionPrice.position_id_fk) & (PositionPrice.currency == currency)
            ).where(
                Position.category_id_fk == category_id_fk
            )
            .offset(offset)
            .limit(limit)
            .order_by(Position.id)
        )
        if not position_without_items:
            stmt = stmt.where(
                exists().where((Item.position_id_fk == Position.id) & (Item.purchase_id_fk.is_(None)))
            )
        return (await self.session.execute(stmt)).all()

    async def get_count_shopping(self, category_id_fk: int, position_without_items: bool) -> int:
        stmt = select(func.count(Position.id)).where(Position.category_id_fk == category_id_fk)
        if not position_without_items:
            stmt = stmt.where(
                exists().where((Item.position_id_fk == Position.id) & (Item.purchase_id_fk.is_(None))))
        return await self.session.scalar(stmt)
