from typing import AsyncIterable

from adaptix import Retort
from aiocryptopay import AioCryptoPay
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage, RedisEventIsolation
from dishka import provide, Provider, Scope
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.bot.dispatcher import get_redis_storage, get_dispatcher
from src.bot.interactors import PaymentInteractor
from src.bot.utilities.media_helper import MediaHelper
from src.cache import Cache
from src.configuration import conf
from src.db import Database
from src.payments import PaymentCreator
from src.translator import Translator


class AiogramProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis_storage(self, redis: Redis) -> RedisStorage:
        return get_redis_storage(
            redis
        )

    @provide
    async def get_event_isolation(self, redis: Redis) -> RedisEventIsolation:
        return RedisEventIsolation(
            redis=redis,
            key_builder=DefaultKeyBuilder(with_destiny=True)
        )

    @provide
    async def get_dp(self, event_isolation: RedisEventIsolation, storage: RedisStorage) -> Dispatcher:
        return get_dispatcher(
            event_isolation=event_isolation,
            storage=storage,
        )

    @provide
    async def get_bot(self) -> Bot:
        return Bot(
            token=conf.bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )


class AdaptixProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_retort(self) -> Retort:
        return Retort()


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_db(self, engine: AsyncEngine) -> AsyncIterable[Database]:
        async with AsyncSession(bind=engine) as session:
            yield Database(session=session)

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncEngine:
        return create_async_engine(url=conf.db.build_connection_str(), echo=conf.log.is_debug,
                                   pool_pre_ping=True)


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_redis(self) -> Redis:
        return Redis(
            db=conf.redis.db,
            host=conf.redis.host,
            password=conf.redis.passwd,
            username=conf.redis.username,
            port=conf.redis.port,
            decode_responses=True
        )


class CacheProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_cache(self, redis: Redis, retort: Retort) -> Cache:
        return Cache(
            redis=redis,
            retort=retort
        )


class TranslatorProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_translator(self) -> Translator:
        return Translator()


class PaymentProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_cb(self) -> AsyncIterable[AioCryptoPay]:
        async with AioCryptoPay(
                token=conf.cb.token,
                network=conf.cb.network
        ) as cryptopay:
            yield cryptopay

    @provide(scope=Scope.REQUEST)
    async def payment_creator(self, aiocryptopay: AioCryptoPay) -> PaymentCreator:
        return PaymentCreator(
            aiocryptopay=aiocryptopay,
        )


class UtilitiesProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_media_fix(self, bot: Bot) -> MediaHelper:
        return MediaHelper(bot)


class InteractorsProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_payment_interactor(self, db: Database, bot: Bot, translator: Translator) -> PaymentInteractor:
        return PaymentInteractor(
            db=db,
            bot=bot,
            translator=translator.t_hub
        )
