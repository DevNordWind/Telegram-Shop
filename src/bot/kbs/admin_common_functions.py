from aiogram.types import KeyboardButton as rkb, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner


def admin_common_functions_kb(translator: TranslatorRunner) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            rkb(text=translator.get('common-functions.find-btn')),
            rkb(text=translator.get('common-functions.mailing-btn'))
        ],
        [
            rkb(
                text=translator.get(
                    'back'
                )
            )
        ]
    ]
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard
    )
