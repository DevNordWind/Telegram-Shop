import logging
import math
from decimal import Decimal

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import User, Message
from fluentogram import TranslatorRunner

from src.db.enums import Currency


# Temporary function
def convert_currency(
        rub_usd_rate: Decimal,
        source: Currency,
        target: Currency,
        amount: Decimal,
        precision: int = 2

) -> Decimal:
    if source == target:
        result = amount
    elif source == Currency.RUB and target == Currency.USD:
        result = amount * rub_usd_rate
    elif source == Currency.USD and target == Currency.RUB:
        result = amount / rub_usd_rate
    else:
        raise ValueError(f"Conversion from {source} to {target} is not supported")

    return result.quantize(Decimal(f"1.{'0' * precision}"))


def get_currency_symbol_by_enum(currency: Currency):
    return {
        Currency.RUB: '₽',
        Currency.USD: '$',
        Currency.EUR: '€',
        Currency.UAH: '₴',
    }[currency]


def get_pages(height: int, items: int) -> int:
    if items / height < 0:
        return 0
    return math.ceil(items / height)


def format_settings_text(
        user: User,
        text: str,
        null_username: str
):
    return text.format(
        username=user.username if user.username else null_username,
        first_name=user.first_name,
        user_id=user.id
    )


def render_settings_text(
        user: User,
        translator: TranslatorRunner,
        text: str
) -> str:
    null_username = translator.get('null-username')
    return text.format(
        first_name=user.first_name,
        username=user.username if user.username else null_username,
        user_id=user.id
    )


async def is_html_valid(event: Message) -> bool:
    try:
        await (await event.answer(event.text)).delete()
        return True
    except TelegramBadRequest as e:
        logging.error(e)
        return False
