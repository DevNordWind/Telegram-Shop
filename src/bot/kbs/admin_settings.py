from aiogram.types import KeyboardButton as rkb
from aiogram.types import ReplyKeyboardMarkup
from fluentogram import TranslatorRunner


def admin_settings_kb(translator: TranslatorRunner) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            rkb(
                text=translator.get('admin-settings.change-data-btn')
            ),
            rkb(
                text=translator.get('admin-settings.switches-btn')
            )
        ],
        [
            rkb(
                text=translator.get('back')
            )
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
