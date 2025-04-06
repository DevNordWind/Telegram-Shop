from dataclasses import dataclass
from decimal import Decimal

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.utilities import get_pages
from src.cache.models import RedisUser, BotSettings
from src.db import Database
from src.db.enums import Currency, Lang
from src.db.models import Purchase


@dataclass
class CurrencyBtn:
    id: str
    name: str
    is_current: bool


def calculate_total(
        user_currency: Currency,
        usd_balance: Decimal,
        rub_balance: Decimal,
        rub_usd: Decimal,
        precision: int = 2
) -> Decimal:
    if user_currency == Currency.RUB:
        if usd_balance > 0:
            result = usd_balance / rub_usd + rub_balance
        else:
            result = rub_balance
    elif user_currency == Currency.USD:
        if rub_balance > 0:
            result = rub_balance * rub_usd + usd_balance
        else:
            result = usd_balance
    return result.quantize(Decimal(f"1.{'0' * precision}"))


@inject
async def profile_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs) -> dict:
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    db_user = await db.user.get_profile_data(redis_user.id)

    usd_balance = 0
    rub_balance = 0
    for user in db_user:
        if user[2] == "RUB":
            rub_balance = user[1]
        elif user[2] == "USD":
            usd_balance = user[1]

    total_amount = calculate_total(
        redis_user.currency,
        usd_balance=usd_balance,
        rub_balance=rub_balance,
        rub_usd=Decimal(bot_settings.rub_usd)
    )

    return {
        'user_id': str(dialog_manager.event.from_user.id),
        'amount': usd_balance if redis_user.currency == Currency.USD else rub_balance,
        'currency': redis_user.currency,
        'count_items': db_user[0][1],
        'total_amount': total_amount,
        'reg_time': db_user[0][3]
    }


@inject
async def purchases_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    widget: ManagedScroll = dialog_manager.find("PURCHASES_SCROLLING")

    current_page: int = await widget.get_page()
    height = 10

    offset = current_page * height

    purchases = await db.purchase.get_list_profile(
        user_id_fk=redis_user.id,
        offset=offset,
        limit=height
    )

    purchases_count = await db.purchase.count(Purchase.user_id_fk == redis_user.id)

    return {
        'btns': [(purchase[0], translator.get(
            'purchases.btn',
            created_at=purchase[3],
            amount=str(purchase[1]),
            currency=purchase[2],
            item_count=str(purchase[4])
        ))
                 for purchase in purchases
                 ],
        'pages': get_pages(height=height, items=purchases_count),
    }


@inject
async def purchase_details_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']

    purchase_id = dialog_manager.dialog_data.get('purchase_id')
    details = await db.purchase.get_details(
        purchase_id,
        redis_user.lang
    )

    return {
        'created_at': details[4],
        'category_name': details[0][0] if details[0][0] is not None else translator.get('relation-removed'),
        'position_name': details[1][0] if details[1][0] is not None else translator.get('relation-removed'),
        'amount': str(details[2]),
        'currency': details[3],
        'id': purchase_id,
        'item_count': str(details[5])
    }


async def change_lang_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    translator = dialog_manager.middleware_data['translator']
    prefix = 'lang-select'
    btns = [
        (translator.get(f'{prefix}.{lang.name}'), lang.value) for lang in Lang
    ]
    return {
        'btns': btns
    }


async def change_currency_btn(dialog_manager: DialogManager, **kwargs) -> dict:
    current_currency: Currency = dialog_manager.middleware_data['redis_user'].currency

    currencies = (Currency.USD, Currency.RUB)
    btns = [
        CurrencyBtn(currency.value, currency.value, currency == current_currency) for currency in currencies
    ]
    return {
        'btns': btns,
    }
