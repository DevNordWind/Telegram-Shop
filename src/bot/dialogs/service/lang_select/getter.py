from aiogram_dialog import DialogManager
from dishka import FromDishka
from fluentogram import TranslatorRunner

from src.db.enums import Lang


async def lang_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    translator = dialog_manager.middleware_data['translator']
    prefix = 'lang-select'
    btns = [
        (translator.get(f'{prefix}.{lang.name}'), lang.value) for lang in Lang
    ]
    return {
        'btns': btns
    }
