from decimal import Decimal
from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import Currency


class Wallet(Base):
    user_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id')
    )
    currency: Mapped[Currency] = mapped_column(
        sa.String(length=4), default="RUB"
    )
    balance: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(16, 2), default=0.00
    )

    user: Mapped["User"] = relationship(
        back_populates='wallet',
        uselist=False
    )

    refill: Mapped[List["Refill"]] = relationship(
        back_populates='wallet',
        uselist=True
    )
