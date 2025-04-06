from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums import Lang, Currency
from src.db.models.base import Base


class PositionLocalized(Base):
    position_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('position.id', ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(
        sa.String, nullable=False
    )
    description: Mapped[str] = mapped_column(
        sa.String, nullable=True
    )
    lang: Mapped[Lang] = mapped_column(
        sa.String(length=4), nullable=False
    )
    position: Mapped["Position"] = relationship(
        back_populates='position_localized',
        uselist=False
    )
