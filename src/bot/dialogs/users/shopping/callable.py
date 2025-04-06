import asyncio
from decimal import Decimal
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from sqlalchemy.orm import selectinload

from src.bot.states import ShoppingState
from src.cache.models import RedisUser
from src.db import Database
from src.db.models import Wallet, Position, PositionPrice, Item, PositionLocalized, User, Purchase


async def on_select_category(event: CallbackQuery, widget: Select, dialog_manager: DialogManager, category_id: int):
    dialog_manager.dialog_data.update(
        {
            'category_id_fk': category_id
        }
    )
    await dialog_manager.switch_to(ShoppingState.select_position)


async def on_select_position(event: CallbackQuery, widget: Select, dialog_manager: DialogManager, position_id: int):
    dialog_manager.dialog_data.update(
        {
            'position_id': position_id
        }
    )
    await dialog_manager.switch_to(ShoppingState.position_details)


@inject
async def on_buy(event: CallbackQuery, widget: Button, dialog_manager: DialogManager, db: FromDishka[Database]):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    position_id: int = int(dialog_manager.dialog_data.get('position_id'))
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    position = await db.position.get_by_where(
        whereclause=Position.id == position_id,
        options=(
            selectinload(Position.position_price.and_(PositionPrice.currency == redis_user.currency)),
            selectinload(Position.position_localized.and_(PositionLocalized.lang == redis_user.lang)),
            selectinload(Position.item.and_(Item.purchase_id_fk == None))
        )
    )
    wallet = await db.wallet.get_by_where(
        (Wallet.user_id_fk == redis_user.id) & (Wallet.currency == redis_user.currency)
    )

    max_possible_count = round(int(wallet.balance / position.position_price[0].price))
    if position.item and len(position.item) < max_possible_count:
        max_possible_count = len(position.item)
    if wallet.balance < position.position_price[0].price:
        return await dialog_manager.switch_to(
            ShoppingState.not_enough_money
        )
    if len(position.item) == 0:
        return await event.message.reply(
            translator.get('position-details.items-missing')
        )

    dialog_manager.dialog_data.update(
        {
            'position_name': position.position_localized[0].name,
            'max_possible_count': max_possible_count,
            'position_price': str(position.position_price[0].price),
            'currency': redis_user.currency,
            'balance': str(wallet.balance),
        }
    )

    if max_possible_count > 1:
        return await dialog_manager.switch_to(
            ShoppingState.input_amount_item
        )
    dialog_manager.dialog_data.update(
        {
            'count_to_buy': 1,
            'amount_to_buy': str(position.position_price[0].price)
        }
    )
    await dialog_manager.switch_to(
        ShoppingState.approve_buy
    )


async def on_item_input_error(event: Message, widget: Any, dialog_manger: DialogManager, error: ValueError):
    translator: TranslatorRunner = dialog_manger.middleware_data['translator']
    return await event.reply(
        translator.get(
            'errors.invalid-int-msg'
        )
    )


async def on_item_input_success(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        items_amount: int,
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    max_possible_count = int(dialog_manager.dialog_data.get('max_possible_count'))

    if items_amount > max_possible_count:
        return await event.reply(
            translator.get('input-amount-item.not-enough-money')
        )

    dialog_manager.dialog_data.update(
        {
            'count_to_buy': items_amount,
            'amount_to_buy': str(
                Decimal(str(dialog_manager.dialog_data.get('position_price'))) * Decimal(str(items_amount)))
        }
    )
    return await dialog_manager.switch_to(
        ShoppingState.approve_buy
    )


@inject
async def on_approve_buy(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']

    count_to_buy: int = int(dialog_manager.dialog_data.get('count_to_buy'))
    amount_to_buy: Decimal = Decimal(dialog_manager.dialog_data.get('amount_to_buy'))
    position_id: int = int(dialog_manager.dialog_data.get('position_id'))

    user = await db.user.get_by_where(
        User.id == redis_user.id,
        options=(
            selectinload(User.wallet.and_(Wallet.currency == redis_user.currency)),
            selectinload(User.purchase)
        )
    )
    items = await db.item.get_many(
        whereclause=(Item.position_id_fk == position_id) & (Item.purchase_id_fk == None),
        limit=count_to_buy,
        order_by=Item.id
    )
    balance_before = user.wallet[0].balance

    balance_after = user.wallet[0].balance - amount_to_buy

    user.wallet[0].balance -= amount_to_buy

    purchase = Purchase(
        balance_before=balance_before,
        balance_after=balance_after,
        amount=amount_to_buy,
        currency=user.currency,
        item=items
    )

    user.purchase.append(
        purchase
    )
    await db.session.flush()
    for item in items:
        item.purchase_id_fk = purchase.id

    items_list = [f'{i}. {items[i].content}' for i in range(0, len(items))]
    message = '\n\n'.join(items_list)
    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for msg in msgs:
        await event.message.answer(
            msg
        )
        await asyncio.sleep(0.1)

    dialog_manager.dialog_data.update(
        {
            'amount': str(purchase.amount),
            'currency': purchase.currency,
            'item_count': str(len(items)),
            'id': str(purchase.id)
        }
    )

    await db.session.commit()
    return await dialog_manager.switch_to(
        ShoppingState.receipt,
        show_mode=ShowMode.DELETE_AND_SEND
    )
