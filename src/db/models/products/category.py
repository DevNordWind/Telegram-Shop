from datetime import datetime
from typing import List

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class Category(Base):
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    category_localized: Mapped[List["CategoryLocalized"]] = relationship(
        back_populates='category',
        uselist=True,
        cascade="all, delete",
    )

    position: Mapped[List["Position"]] = relationship(
        back_populates='category',
        uselist=True,
        cascade="all, delete",
    )

    item: Mapped[List["Item"]] = relationship(
        back_populates='category',
        uselist=True,
        cascade="all, delete",
    )
