import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..enums import RefillStatus, RefillCause, Currency
from ..models import Refill
from ...payments.enums import PaymentMethod


class RefillRepo(Repository[Refill]):
    type_model = Refill
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Refill, session=session)

    async def new(
            self,
            user_id_fk: int,
            wallet_id_fk: int,
            amount: Decimal,
            currency: Currency,
            status: RefillStatus,
            cause: RefillCause,
            payment_method: PaymentMethod | None = None,
            external_id: str | None = None
    ) -> Refill:
        refill = Refill(
            user_id_fk=user_id_fk,
            wallet_id_fk=wallet_id_fk,
            amount=amount,
            currency=currency,
            status=status,
            cause=cause,
            payment_method=payment_method,
            external_id=external_id
        )
        return await self.session.merge(refill)

    async def get_status(self, refill_id: str) -> RefillStatus:
        stmt = select(Refill.status).where(Refill.id == refill_id)
        return await self.session.scalar(stmt)
