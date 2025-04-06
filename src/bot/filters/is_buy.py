from aiogram.filters import Filter
from aiogram.types import TelegramObject

from src.cache.models import BotSettings


class IsBuyFilter(Filter):
    async def __call__(self, event: TelegramObject, bot_settings: BotSettings, **kwargs):
        if not bot_settings.status_buy:
            return True
        return False
