import json

from adaptix import Retort
from aiogram.enums import ContentType
from redis.asyncio import Redis

from .abstract import Repository
from ..models import BotSettings


class BotSettingsRepo(Repository[BotSettings]):

    def __init__(self, redis: Redis, retort: Retort):
        super().__init__(type_model=BotSettings, redis=redis, retort=retort)

    async def new(self,
                  status_work: bool = True,
                  status_refill: bool = False,
                  status_buy: bool = False,
                  status_cryptobot: bool = False,
                  support: str | None = None,
                  category_without_items: bool = False,
                  position_without_items: bool = False,
                  start_text_ru: str | None = None,
                  start_text_en: str | None = None,
                  faq_text_ru: str | None = None,
                  faq_text_en: str | None = None,
                  start_media_id: str | None = None,
                  start_media_path: str | None = None,
                  start_media_content_type: ContentType | None = None,
                  rub_usd: str = '0.011'
                  ) -> BotSettings:
        bot_settings = BotSettings(
            status_work=status_work,
            status_buy=status_buy,
            status_refill=status_refill,
            status_cryptobot=status_cryptobot,
            support=support,
            category_without_items=category_without_items,
            position_without_items=position_without_items,
            start_text_ru=start_text_ru,
            start_text_en=start_text_en,
            faq_text_ru=faq_text_ru,
            faq_text_en=faq_text_en,
            start_media_id=start_media_id,
            start_media_path=start_media_path,
            start_media_content_type=start_media_content_type,
            rub_usd=rub_usd
        )

        await self.redis.set(bot_settings.build_key(), value=json.dumps(bot_settings.__dict__))

        return bot_settings
