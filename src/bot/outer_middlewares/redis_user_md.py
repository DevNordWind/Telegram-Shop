from collections.abc import Awaitable, Callable
from typing import Any, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import CallbackQuery, Message, ErrorEvent
from dishka.integrations.aiogram import CONTAINER_NAME

from src.cache import Cache


class RedisUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | ErrorEvent,
            data: Dict
    ) -> Any:
        cache: Cache = await data[CONTAINER_NAME].get(Cache)
        event_context: EventContext = data['event_context']
        data['redis_user'] = await cache.user.get_by_key(f'user:{event_context.user.id}')
        return await handler(event, data)
