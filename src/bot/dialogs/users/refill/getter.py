from aiogram_dialog import DialogManager

from src.cache.models import BotSettings


async def select_payment_method_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    return {
        **bot_settings.__dict__
    }


async def refill_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    dialog_manager.dialog_data.update(
        {
            'is_refill_enable': (bot_settings.status_steam or bot_settings.status_cryptobot) and bot_settings.status_refill
        }
    )
    return {
        'is_refill_enable': (bot_settings.status_steam or bot_settings.status_cryptobot) and bot_settings.status_refill
    }
