from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models import Wallet
from .abstract import Repository


class WalletRepo(Repository[Wallet]):
    """Repository abstract class."""

    type_model: type[Wallet]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        super().__init__(type_model=Wallet, session=session)

    async def get_with_refill(self, whereclause):
        stmt = select(Wallet).options(selectinload(Wallet.refill)).where(whereclause)
        return await self.session.scalar(stmt)