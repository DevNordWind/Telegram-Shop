from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Case, Format

from src.bot.dialogs.users.faq.getter import faq_getter
from src.bot.states import FaqState
from src.bot.widgets import GetText

faq = Window(
    Case(
        {
            True: Format('{faq_text}'),
            ...: GetText('default-faq')
        },
      selector=lambda data, widget, manager: bool(data['faq_text'])
    ),

    getter=faq_getter,
    state=FaqState.faq
)