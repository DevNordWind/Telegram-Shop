from aiogram.types import KeyboardButton as rkb, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner

buttons = {
    "buy": "main.buy-btn",
    "profile": "main.profile-btn",
    "support": "main.support-btn",
    "faq": "main.faq-btn",
    "item_management": "main.item-management-btn",
    "statistic": "main.statistic-btn",
    "admin-settings": "main.settings-btn",
    "common_functions": "main.common-functions-btn",
    "payment_systems": "main.payment-systems-btn",
    'settings': 'main.settings-btn'
}


def menu_frep(is_admin: bool, translator: TranslatorRunner) -> ReplyKeyboardMarkup:
    keyboard = [
        [rkb(text=translator.get(buttons["buy"])), rkb(text=translator.get(buttons["profile"]))],
        [rkb(text=translator.get(buttons["support"])), rkb(text=translator.get(buttons["faq"]))],
    ]

    if is_admin:
        keyboard.append(
            [
                rkb(text=translator.get(buttons["item_management"])),
                rkb(text=translator.get(buttons["statistic"]))
            ]
        )
        keyboard.append(
            [
                rkb(text=translator.get(buttons['settings'])),
                rkb(text=translator.get(buttons["common_functions"])),
                rkb(text=translator.get(buttons["payment_systems"])),
            ]
        )

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
