import uuid
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import Currency


class Purchase(Base):
    id: Mapped[UUID] = mapped_column(
        sa.UUID, primary_key=True, default=uuid.uuid4,
    )
    user_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('user.id')
    )

    balance_before: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(10, 2), nullable=False
    )

    balance_after: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(10, 2), nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(10, 2), nullable=False
    )

    currency: Mapped[Currency] = mapped_column(
        sa.String(length=4)
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )

    item: Mapped[List['Item']] = relationship(
        back_populates='purchase',
        uselist=True
    )

    user: Mapped["User"] = relationship(
        back_populates='purchase',
        uselist=False
    )
