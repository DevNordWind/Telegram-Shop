from decimal import Decimal

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from sqlalchemy.orm import selectinload, joinedload

from src.cache.models import RedisUser
from src.db import Database
from src.db.enums import Currency, RefillCause
from src.db.models import User, Purchase, Refill, Item, Position, PositionLocalized, PositionPrice
from .callable import generate_user_whereclause


def refill_count(refills: list[Refill]) -> tuple[int, int]:
    total_give, total_refill = 0, 0
    for refill in refills:
        if refill.cause == RefillCause.GIFT:
            total_give += refill.amount
        total_refill += refill.amount
    return total_give, total_refill


@inject
async def user_profile_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    whereclause = generate_user_whereclause(
        dialog_manager.dialog_data.get('user_id')
    )

    user = await db.user.get_by_where(
        whereclause,
        options=(
            selectinload(User.wallet), selectinload(User.refill),
            selectinload(User.purchase).selectinload(Purchase.item))
    )
    rub_wallet = None
    usd_wallet = None
    for wallet in user.wallet:
        if wallet.currency == Currency.USD:
            usd_wallet = wallet
        if wallet.currency == Currency.RUB:
            rub_wallet = wallet
    total_give, total_refill = refill_count(refills=user.refill)

    return {
        'first_name': user.first_name,
        'user_id': str(user.user_id),
        'username': str(user.username),
        'reg_time': user.reg_time,
        'rub_wallet_amount': str(rub_wallet.balance),
        'usd_wallet_amount': str(usd_wallet.balance),
        'total_give': str(total_give),
        'total_refill': str(total_refill),
        'items_amount': sum(len(purchase.item) for purchase in user.purchase) if user.purchase else '0',
        'currency': user.currency,
    }


async def select_currency_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'btns': [
            (
                Currency.RUB.value
            ),
            (
                Currency.USD.value
            )
        ]
    }


@inject
async def mailing_approve_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    return {
        'users_count': await db.user.count(User.is_active == True)
    }


@inject
async def refill_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    refill = await db.refill.get_by_where(
        Refill.id == dialog_manager.dialog_data.get('refill_id'),
        options=joinedload(Refill.user)
    )
    return {
        'id': str(refill.id),
        'username': str(refill.user.username),
        'user_id': str(refill.user.user_id),
        'amount': refill.amount,
        'currency': refill.currency,
        'payment_method': refill.payment_method if refill.payment_method else "None",
        'comment': str(refill.comment),
        'created_at': refill.created_at
    }

@inject
async def purchase_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    purchase = await db.purchase.get_by_where(
        Purchase.id == dialog_manager.dialog_data.get('purchase_id'),
        options=(joinedload(Purchase.user))
    )
    items = await db.item.get_many(
        Item.purchase_id_fk == purchase.id,
        limit=999
    )
    item = await db.item.get_by_where(
        Item.id == items[0].id,
        options=(
            joinedload(Item.position).selectinload(Position.position_localized.and_(PositionLocalized.lang == redis_user.lang)),
            joinedload(Item.position).selectinload(Position.position_price.and_(PositionPrice.currency == purchase.currency)))
    )
    return {
        'id': str(purchase.id),
        'username': purchase.user.username,
        'user_id': str(purchase.user.user_id),
        'position_name': item.position.position_localized[0].name if item.position else translator.get('relation-removed'),
        'items_count': len(items),
        'item_amount': purchase.amount / Decimal(str(len(items))),
        'items_amount': purchase.amount,
        'currency': purchase.currency,
        'balance_after': purchase.balance_after,
        'balance_before': purchase.balance_before,
        'created_at': purchase.created_at,
    }
