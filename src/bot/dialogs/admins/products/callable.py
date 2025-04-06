from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.db.enums import Lang


async def on_change_lang(event: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    current_lang: Lang = dialog_manager.middleware_data['redis_user'].lang
    temp_lang = dialog_manager.dialog_data.get('temp_lang')
    if temp_lang is None:
        return dialog_manager.dialog_data.update(
            {
                'temp_lang': Lang.EN if current_lang == Lang.RU else Lang.RU
            }
        )
    dialog_manager.dialog_data.pop('temp_lang')
