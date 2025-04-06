from aiogram.filters import Filter
from aiogram.types import TelegramObject

from src.cache.models import BotSettings, RedisUser
from src.db.enums import Role


class IsWorkFilter(Filter):
    async def __call__(self,
                       event: TelegramObject,
                       bot_settings: BotSettings,
                       redis_user: RedisUser | None,
                       **kwargs
                       ):
        if not bot_settings.status_work:
            return False
        return not (redis_user and redis_user.role == Role.ADMINISTRATOR)

