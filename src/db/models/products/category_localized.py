import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enums import Lang
from src.db.models.base import Base


class CategoryLocalized(Base):

    category_id_fk: Mapped[int] = mapped_column(
        sa.ForeignKey('category.id', ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(
        sa.String(length=256)
    )
    lang: Mapped[Lang] = mapped_column(
        sa.String(length=4)
    )
    category: Mapped["Category"] = relationship(
        back_populates='category_localized',
        uselist=False
    )
