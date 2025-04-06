from aiogram import Dispatcher, Bot
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand
from redis.asyncio import Redis

from src.configuration import conf
from .dialogs import *
from .filters import *
from .handlers import *
from .handlers.errors import on_error
from .outer_middlewares import *


def get_redis_storage(
        redis: Redis, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl
) -> RedisStorage:
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl,
                        key_builder=DefaultKeyBuilder(with_destiny=True))


async def on_startup(bot: Bot):
    await set_commands(bot)


async def set_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start', description='♻️ Перезапустить бота',
            ),
        ],
        language_code='ru'
    )

    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start', description='♻️ Restart bot',
            ),
        ],
        language_code='en'
    )


def get_dispatcher(
        storage: BaseStorage,
        fsm_strategy: FSMStrategy = FSMStrategy.CHAT,
        event_isolation: BaseEventIsolation = None,
) -> Dispatcher:
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation,
    )
    register_outer_middlewares(dp)

    dp.error.register(
        on_error, ExceptionTypeFilter(Exception)
    )
    dp.include_router(service_router)
    dp.include_routers(*service_dialogs)

    dp.include_router(start_router)
    dp.include_routers(*users_dialogs)

    for dialog in admin_dialogs:
        dialog.message.filter(IsAdminFilter())
        dialog.callback_query.filter(IsAdminFilter())
        dp.include_router(dialog)

    dp.startup.register(on_startup)

    return dp


def register_outer_middlewares(dp: Dispatcher):
    for outer_middleware in (
    RedisUserMiddleware, RegisterMiddleware, BotSettingsMiddleware, IsActiveMd, TranslatorMiddleware):
        dp.message.outer_middleware(outer_middleware())
        dp.callback_query.outer_middleware(outer_middleware())
        dp.errors.outer_middleware(outer_middleware())

