from aiogram.filters import Filter
from aiogram.types import TelegramObject, CallbackQuery
from aiogram_dialog.api.entities import Context

from src.bot.states import SelectLangState
from src.cache.models import RedisUser


class IsSelectLangFilter(Filter):
    async def __call__(self, event: TelegramObject, redis_user: RedisUser, aiogd_context: None | Context):
        if redis_user and not redis_user.lang:
            if aiogd_context and aiogd_context.state == SelectLangState.select_lang:
                if isinstance(event, CallbackQuery):
                    return False
            return True
        return False
