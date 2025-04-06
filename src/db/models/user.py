from datetime import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import Currency, Lang, Role


class User(Base):
    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        sa.String(length=32), nullable=True, unique=False
    )
    first_name: Mapped[str] = mapped_column(
        sa.String(length=64), nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        sa.String(length=64), nullable=True
    )

    """ Selected currency for payment.ftl"""
    currency: Mapped[Currency] = mapped_column(
        sa.String(length=4), default="RUB"
    )

    lang: Mapped[Lang] = mapped_column(
        sa.String(length=4), nullable=True
    )

    role: Mapped[Role] = mapped_column(
        sa.String, nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        sa.Boolean, default=True, nullable=False
    )

    reg_time: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )

    """ One-to-many relationship"""

    wallet: Mapped[List["Wallet"]] = relationship(
        back_populates='user',
        uselist=True
    )

    refill: Mapped[List["Refill"]] = relationship(
        back_populates='user',
        uselist=True
    )

    purchase: Mapped[List["Purchase"]] = relationship(
        back_populates='user',
        uselist=True
    )
