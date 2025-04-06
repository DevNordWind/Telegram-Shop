from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, ErrorEvent
from dishka.integrations.aiogram import CONTAINER_NAME

from src.cache import Cache


class BotSettingsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | ErrorEvent,
            data: Dict
    ) -> Any:
        cache: Cache = await data[CONTAINER_NAME].get(Cache)
        data['bot_settings'] = await cache.bot_settings.get_by_key('settings')
        return await handler(event, data)
