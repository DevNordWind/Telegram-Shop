from adaptix import Retort
from redis.asyncio import Redis

from .repos import *


class Cache:
    user: UserRepo
    bot_settings: BotSettingsRepo

    def __init__(
            self,
            redis: Redis,
            retort: Retort,
            user: UserRepo = None,
            bot_settings: BotSettingsRepo = None
    ):
        self.user = user or UserRepo(redis=redis, retort=retort)
        self.bot_settings = bot_settings or BotSettingsRepo(redis=redis, retort=retort)
