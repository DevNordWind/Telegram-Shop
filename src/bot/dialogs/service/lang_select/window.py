from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from src.bot.states import SelectLangState
from src.bot.widgets import GetText
from .callable import on_lang_select
from .getter import lang_getter

lang_select_window = Window(
    GetText(
        'lang-select'
    ),

    Select(
        Format('{item[0]}'),
        id='lang_select_items',
        on_click=on_lang_select,
        item_id_getter=lambda x: x[1],
        items='btns'
    ),

    getter=lang_getter,
    state=SelectLangState.select_lang
)
