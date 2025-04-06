from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.filters import Filter
from aiogram.types import TelegramObject

from src.cache.models import RedisUser
from src.configuration import conf
from src.db.enums import Role


class IsAdminFilter(Filter):
    async def __call__(self, event: TelegramObject, event_context: EventContext, redis_user: RedisUser):
        if not redis_user:
            return event_context.user.id in conf.admin.admins()
        return Role.ADMINISTRATOR == redis_user.role
