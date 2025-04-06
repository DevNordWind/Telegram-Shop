from fluentogram import TranslatorRunner
from aiogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup


def tech_work_support_kb(translator: TranslatorRunner, support: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            ikb(
                text=translator.get('tech-work.send-message-support'),
                url=f't.me/{support}'
            )
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )