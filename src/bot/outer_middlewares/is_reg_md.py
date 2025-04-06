from collections.abc import Awaitable, Callable
from typing import Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, ErrorEvent
from aiogram.types import User as AioUser
from dishka import AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME

from src.cache import Cache
from src.cache.models import RedisUser
from src.configuration import conf
from src.db import Database
from src.db.enums import Role, Currency
from src.db.models import User


class RegisterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | ErrorEvent,
            data: Dict
    ) -> Any:
        aiogram_user: AioUser = data['event_context'].user
        async_container: AsyncContainer = data[CONTAINER_NAME]
        redis_user: RedisUser | None = data.get('redis_user')
        cache: Cache = await async_container.get(Cache)
        db: Database = await async_container.get(Database)
        if not redis_user:
            redis_user: RedisUser = await self.register(
                aiogram_user, db, cache
            )
            data['redis_user']: RedisUser = redis_user
        else:
            await self.handle_user_data(
                aio_user=aiogram_user,
                db=db,
                cache=cache,
                redis_user=redis_user
            )
        return await handler(event, data)

    async def register(self, aio_user: AioUser, db: Database, cache: Cache) -> RedisUser:
        db_user: User | None = await db.user.get_by_where(User.user_id == aio_user.id)
        if not db_user:
            role: Role = Role.ADMINISTRATOR if conf.admin.is_admin(aio_user.id) else Role.USER
            currency: Currency = Currency.RUB
            user = await db.user.new_with_wallet(
                user_id=aio_user.id,
                first_name=aio_user.first_name,
                role=role,
                currency=currency,
                last_name=aio_user.last_name,
                username=aio_user.username
            )
            await db.session.flush()

            redis_user = await cache.user.new(
                user_id=aio_user.id,
                id=user.id,
                first_name=aio_user.first_name,
                currency=user.currency,
                role=role,
                username=aio_user.username,
                last_name=aio_user.last_name
            )
            await db.session.commit()
            return redis_user
        else:
            return await cache.user.new(
                user_id=db_user.user_id,
                id=db_user.id,
                first_name=db_user.first_name,
                currency=db_user.currency,
                lang=db_user.lang,
                role=db_user.role,
                username=db_user.username,
                last_name=db_user.last_name
            )

    async def handle_user_data(self,
                               aio_user: AioUser,
                               db: Database,
                               cache: Cache,
                               redis_user: RedisUser
                               ):
        keys = ['last_name', 'username']
        need_commit = False
        for key in keys:
            redis_atr = getattr(redis_user, key)
            aio_atr = getattr(aio_user, key)
            if redis_atr != aio_atr:
                need_commit = True
                data = {key: aio_atr}
                await db.user.update(User.id == redis_user.id, values=data)
                redis_user.__dict__.update(data)
                await cache.user.update_model(redis_user, key=aio_user.id)
        if need_commit:
            await db.session.commit()
