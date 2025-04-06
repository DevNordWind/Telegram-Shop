import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from src.bot.on_startup import on_startup
from src.configuration import conf
from src.providers import DatabaseProvider, AdaptixProvider, AiogramProvider, CacheProvider, TranslatorProvider, \
    PaymentProvider, UtilitiesProvider, RedisProvider, InteractorsProvider


async def main():
    async_container = make_async_container(
        DatabaseProvider(),
        AdaptixProvider(),
        AiogramProvider(),
        RedisProvider(),
        CacheProvider(),
        TranslatorProvider(),
        InteractorsProvider(),
        PaymentProvider(),
        UtilitiesProvider()
    )
    dp, bot = await async_container.get(Dispatcher), await async_container.get(Bot)
    bot_info = await bot.get_me()
    setup_dishka(async_container, dp)
    setup_dialogs(dp)
    await on_startup(async_container)
    conf.log.setup_logger()

    logging.info("%s is running on the username @%s!", bot_info.first_name, bot_info.username)
    return await dp.start_polling(
        bot
    )


if __name__ == '__main__':
    asyncio.run(main())
