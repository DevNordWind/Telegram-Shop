from aiogram.types import KeyboardButton as rkb, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner


def admin_products_kb(translator: TranslatorRunner):
    keyboard = [
        [
            rkb(
                text=translator.get('product-management.create-position-btn')
            ),
            rkb(
                text=translator.get('product-management.edit-position-btn')
            ),
        ],
        [
            rkb(
                text=translator.get('product-management.create-category-btn')
            ),
            rkb(
                text=translator.get('product-management.edit-category-btn')
            )
        ],
        [
            rkb(
                text=translator.get('product-management.add-item-btn')
            ),
            rkb(
                text=translator.get('product-management.deleting-btn')
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
