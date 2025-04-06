from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums import Currency
from src.db.models.base import Base


class PositionPrice(Base):
    position_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('position.id', ondelete="CASCADE")
    )
    price: Mapped[Decimal] = mapped_column(
        sa.DECIMAL(10, 2), nullable=False
    )
    currency: Mapped[Currency] = mapped_column(
        sa.String(length=4), nullable=False
    )
    position: Mapped["Position"] = relationship(
        back_populates='position_price',
        uselist=False
    )
