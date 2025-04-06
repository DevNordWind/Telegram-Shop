from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from ..enums import WithdrawStatus, WithdrawCause
from ..models import Withdraw


class WithdrawRepo(Repository[Withdraw]):
    type_model = Withdraw
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=Withdraw, session=session)

    async def new(self,
                  user_id_fk: int,
                  wallet_id_fk: int,
                  amount: Decimal,
                  cause: WithdrawCause,
                  status: WithdrawStatus
                  ) -> Withdraw:
        withdraw = Withdraw(
            user_id_fk=user_id_fk,
            wallet_id_fk=wallet_id_fk,
            amount=amount,
            cause=cause,
            status=status
        )
        return await self.session.merge(withdraw)
