from aiocryptopay import AioCryptoPay
from aiocryptopay.exceptions import CodeErrorFactory
from aiocryptopay.models.profile import Profile
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.cache import Cache
from src.cache.models import BotSettings
from src.configuration import conf


async def cryptobot_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'payment_method': "CryptoBot",
        **dialog_manager.middleware_data['bot_settings'].__dict__
    }


@inject
async def cryptobot_info_getter(dialog_manager: DialogManager, cb: FromDishka[AioCryptoPay], cache: FromDishka[Cache],
                                **kwargs):
    try:
        profile: Profile = await cb.get_me()
        return {
            **profile.__dict__,
            'token': conf.cb.token
        }
    except CodeErrorFactory as e:
        if e.code == 401:
            bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
            bot_settings.status_cryptobot = not bot_settings.status_cryptobot
            await cache.bot_settings.update_model(bot_settings)
            return {
                'profile': None
            }
