import uuid
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import RefillStatus, RefillCause, Currency


class Refill(Base):
    id: Mapped[UUID] = mapped_column(
        sa.UUID, primary_key=True, default=uuid.uuid4,
    )
    user_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id')
    )
    wallet_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('wallet.id')
    )

    ''' Id from payment system(optional) '''
    external_id: Mapped[str] = mapped_column(
        sa.String, nullable=True
    )

    amount: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(16, 2)
    )

    currency: Mapped[Currency] = mapped_column(
        sa.String, nullable=False
    )

    status: Mapped[RefillStatus] = mapped_column(
        sa.String, nullable=False, default=RefillStatus.PENDING
    )

    cause: Mapped[RefillCause] = mapped_column(
        sa.String, nullable=False, default=RefillCause.PAYMENT
    )

    payment_method: Mapped[str] = mapped_column(
        sa.String, nullable=True
    )

    comment: Mapped[str] = mapped_column(
        sa.String, nullable=True
    )

    created_at: Mapped[str] = mapped_column(
        sa.DateTime, default=datetime.now()
    )

    wallet: Mapped["Wallet"] = relationship(
        back_populates='refill',
        uselist=False
    )
    user: Mapped["User"] = relationship(
        back_populates='refill',
        uselist=False
    )
