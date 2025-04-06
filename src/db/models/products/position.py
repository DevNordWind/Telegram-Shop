from datetime import datetime
from typing import List

import sqlalchemy as sa
from aiogram.enums import ContentType
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class Position(Base):
    category_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('category.id', ondelete="CASCADE")
    )
    file_path: Mapped[str] = mapped_column(
        sa.String, nullable=True
    )
    file_id: Mapped[str] = mapped_column(
        sa.String, nullable=True,
    )
    content_type: Mapped[ContentType] = mapped_column(
        sa.String, nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    position_localized: Mapped[List["PositionLocalized"]] = relationship(
        back_populates='position',
        uselist=True,
        cascade="all, delete",
    )

    position_price: Mapped[List["PositionPrice"]] = relationship(
        back_populates='position',
        uselist=True,
        cascade="all, delete"
    )

    category: Mapped["Category"] = relationship(
        back_populates='position',
        uselist=False
    )

    item: Mapped[List["Item"]] = relationship(
        back_populates='position',
        uselist=True,
        cascade="all, delete",
    )
