from dataclasses import dataclass

from aiogram.enums import ContentType

from ..models import Base


@dataclass
class BotSettings(Base):
    status_work: bool = True
    status_refill: bool = False
    status_buy: bool = False
    status_cryptobot: bool = False
    status_steam: bool = False
    support: str | None = None
    category_without_items: bool = False
    position_without_items: bool = False
    start_text_ru: str | None = None
    start_text_en: str | None = None
    faq_text_ru: str | None = None
    faq_text_en: str | None = None
    start_media_id: str | None = None
    start_media_path: str | None = None
    start_media_content_type: ContentType | None = None
    rub_usd: str = '0.011'

    @staticmethod
    def build_key(*args) -> str:
        return 'settings'
