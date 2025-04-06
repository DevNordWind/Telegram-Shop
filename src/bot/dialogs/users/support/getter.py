from aiogram_dialog import DialogManager

from src.cache.models import bot_settings


async def support_getter(dialog_manager: DialogManager, **kwargs):
    return {
        **dialog_manager.middleware_data['bot_settings'].__dict__
    }