from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Case, Format

from src.bot.dialogs.users.support.getter import support_getter
from src.bot.states import SupportState
from src.bot.widgets import GetText

support = Window(
    Case(
        {
            True: GetText('support'),
            ...: GetText('default-support')
        },
        selector=lambda data, widget, manager: bool(data['support'])
    ),

    Url(
        text=GetText('support.message-support-btn'),
        url=Format('t.me/{support}'),
        when=F['support'].is_not(None)
    ),

    getter=support_getter,
    state=SupportState.support
)
