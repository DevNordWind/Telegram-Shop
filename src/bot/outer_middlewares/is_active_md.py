from collections.abc import Awaitable, Callable
from typing import Any, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import CallbackQuery, Message, ErrorEvent
from dishka.integrations.aiogram import CONTAINER_NAME

from src.cache import Cache
from src.cache.models import RedisUser
from src.db import Database
from src.db.models import User


class IsActiveMd(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | ErrorEvent,
            data: Dict
    ) -> Any:
        redis_user: RedisUser = data['redis_user']
        if not redis_user.is_active:
            db: Database = await data[CONTAINER_NAME].get(Database)
            cache: Cache = await data[CONTAINER_NAME].get(Cache)
            event_context: EventContext = data['event_context']
            await db.user.update(User.id == redis_user.id, values={"is_active": True})
            redis_user.is_active = True
            await cache.user.update_model(redis_user, f'{event_context.user.id}')
            await db.session.commit()
        return await handler(event, data)
