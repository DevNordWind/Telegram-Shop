from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select, func, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .abstract import Repository
from ..enums import Currency, Lang, Role
from ..models import User
from ..models import Wallet
from ..models.purchase import Purchase


class UserRepo(Repository[User]):
    """Repository abstract class."""

    type_model: type[User]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        super().__init__(type_model=User, session=session)

    async def new(
            self,
            user_id: int,
            first_name: str,
            role: Role,
            currency: Currency | None = None,
            lang: Lang | None = None,
            last_name: str | None = None,
            username: str | None = None
    ) -> User:
        return await self.session.merge(
            User(
                user_id=user_id,
                first_name=first_name,
                role=role,
                currency=currency,
                lang=lang,
                last_name=last_name,
                username=username
            )
        )

    async def new_with_wallet(
            self,
            user_id: int,
            first_name: str,
            role: Role,
            currency: Currency | None = None,
            lang: Lang | None = None,
            last_name: str | None = None,
            username: str | None = None
    ) -> User:
        user = User(
            user_id=user_id,
            first_name=first_name,
            role=role,
            currency=currency,
            lang=lang,
            last_name=last_name,
            username=username
        )
        for currency in Currency:
            user.wallet.append(
                Wallet(
                    currency=currency
                )
            )
        return await self.session.merge(user)

    async def get_with_wallet_refill(self, user_id: int) -> User:
        stmt = select(User).options(selectinload(User.wallet, User.refill)).where(User.id == user_id)
        return await self.session.scalar(
            stmt
        )

    async def get_profile_data(self, user_id: int) -> Sequence[Row[tuple[Any, Any, Any, Any, Any]]]:
        stmt = select(
            func.count(Purchase.id).label("purchase_count"),
            Wallet.balance.label("balance"),
            Wallet.currency.label("wallet_currency"),
            User.reg_time,
        ).outerjoin(
            Purchase, User.id == Purchase.user_id_fk
        ).join(
            Wallet,
            User.id == Wallet.user_id_fk
        ).where(
            User.id == user_id,
            Wallet.currency.in_(("USD", "RUB"))
        ).group_by(
            User.id,
            Wallet.balance,
            Wallet.currency
        )

        return (await self.session.execute(stmt)).all()

    async def get_statistics(self):
        stmt = select(User)
        now = datetime.now()
        result = (await self.session.scalars(stmt)).all()

