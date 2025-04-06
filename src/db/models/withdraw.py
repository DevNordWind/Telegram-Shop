import uuid
from decimal import Decimal
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from ..enums.withdraw_enums import WithdrawCause, WithdrawStatus


class Withdraw(Base):
    id: Mapped[UUID] = mapped_column(
        sa.UUID, primary_key=True, default=uuid.uuid4
    )
    user_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id')
    )
    wallet_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('wallet.id')
    )
    amount: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(16, 2)
    )
    cause: Mapped[WithdrawCause] = mapped_column(
        sa.String, default=WithdrawCause.ADMINS_DECISION, nullable=False
    )
    status: Mapped[WithdrawStatus] = mapped_column(
        sa.String, nullable=False
    )