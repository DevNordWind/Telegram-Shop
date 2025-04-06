from fluentogram import TranslatorRunner
from aiogram.types import KeyboardButton as rkb, ReplyKeyboardMarkup


def admin_payments_kb(translator: TranslatorRunner) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            rkb(
                text=translator.get('payment.cb-btn'),
            ),
        ],
        [
            rkb(
                text=translator.get('back')
            )
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
