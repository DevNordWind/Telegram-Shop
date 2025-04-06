from datetime import datetime
from typing import List

import sqlalchemy as sa
from aiogram.enums import ContentType
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class Item(Base):
    category_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('category.id', ondelete='SET NULL'), nullable=True
    )
    position_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('position.id', ondelete="SET NULL"), nullable=True
    )
    purchase_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('purchase.id', ondelete="NO ACTION"), nullable=True
    )
    content: Mapped[str] = mapped_column(
        sa.String, nullable=False
    )
    content_type: Mapped[ContentType] = mapped_column(
        sa.String, nullable=False, default=ContentType.TEXT
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    category: Mapped["Category"] = relationship(
        back_populates='item',
        uselist=False
    )
    position: Mapped["Position"] = relationship(
        back_populates="item",
        uselist=False
    )
    purchase: Mapped["Purchase"] = relationship(
        back_populates='item',
        uselist=False
    )