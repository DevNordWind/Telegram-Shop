from aiogram_dialog import DialogManager

from src.cache.models import RedisUser, BotSettings
from src.db.enums import Lang


async def faq_getter(dialog_manager: DialogManager, **kwargs):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']

    faq_text = None
    if bot_settings.faq_text_ru and bot_settings.faq_text_en:
        faq_text = bot_settings.faq_text_ru if redis_user.lang == Lang.RU else bot_settings.faq_text_en

    return {
        'faq_text': faq_text
    }