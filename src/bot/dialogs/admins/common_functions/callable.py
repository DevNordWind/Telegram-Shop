import asyncio
import uuid
from contextlib import suppress
from decimal import Decimal

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter, TelegramForbiddenError
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from sqlalchemy.orm import selectinload

from src.bot.states import CommonFunctionsState
from src.bot.utilities import MediaHelper
from src.cache import Cache
from src.db import Database
from src.db.enums import Currency, RefillStatus, RefillCause, WithdrawStatus, WithdrawCause
from src.db.models import User, Wallet, Purchase, Refill, Item
from src.translator import Translator


def is_uuid(value: str) -> bool:
    try:
        uuid_obj = uuid.UUID(value, version=4)
        return str(uuid_obj) == value
    except ValueError:
        return False


def is_postgres_bigint(value: int) -> bool:
    return -(2 ** 63) <= value <= (2 ** 63 - 1)


def generate_user_whereclause(input: str | int) -> str:
    if input.isdigit():
        input = int(input)
        if is_postgres_bigint(input):
            whereclause = User.user_id == input
        else:
            whereclause = User.id == input
    else:
        if '@' in input:
            input = input.replace('@', '')
        whereclause = User.username == input
    return whereclause


@inject
async def on_input_find(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        input: str,
        db: FromDishka[Database]
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    if input.startswith('#'):
        input = input.replace('#', '')
    if is_uuid(input):
        purchase = await db.purchase.get_by_where(Purchase.id == input)
        refill = await db.refill.get_by_where(Refill.id == input)
        if not purchase and not refill:
            return await event.reply(
                translator.get('find.not-found')
            )
        dialog_manager.dialog_data.update(
            {
                'purchase_id': str(purchase.id) if purchase else None,
                'refill_id': str(refill.id) if refill else None
            }
        )
        if purchase:
            return await dialog_manager.switch_to(CommonFunctionsState.purchase)
        if refill:
            return await dialog_manager.switch_to(CommonFunctionsState.refill)
    user = await db.user.is_exists(generate_user_whereclause(input))
    if not user or user is None:
        return await event.reply(
            translator.get('find.not-found')
        )
    dialog_manager.dialog_data.update(
        {
            'user_id': input,
        }
    )
    return await dialog_manager.switch_to(
        CommonFunctionsState.user_profile
    )


@inject
async def on_unload_items(event: CallbackQuery, widget: Button, dialog_manager: DialogManager,
                          db: FromDishka[Database]):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    purchase_id_fk: str = str(dialog_manager.dialog_data.get('purchase_id'))
    items = await db.item.get_many(
        whereclause=Item.purchase_id_fk == purchase_id_fk,
        limit=99999,
        order_by=Item.id
    )

    items_list = [f'{i}. {items[i].content}' for i in range(0, len(items))]
    message = '\n\n'.join(items_list)
    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for msg in msgs:
        await event.message.answer(
            msg
        )
        await asyncio.sleep(0.1)


async def on_select_currency(event: CallbackQuery, widget: Select, dialog_manager: DialogManager, currency: Currency):
    dialog_manager.dialog_data.update(
        {
            'currency': currency
        }
    )
    await dialog_manager.switch_to(
        CommonFunctionsState.input_amount_change_balance
    )


async def on_input_amount_error(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    return await event.reply(
        text=translator.get('errors.invalid-number-msg')
    )


async def on_balance_actions(event: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(
        {
            'operation': widget.widget_id
        }
    )


@inject
async def on_input_amount_success(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        amount: Decimal,
        db: FromDishka[Database],
):
    bot, translator = dialog_manager.middleware_data['bot'], dialog_manager.middleware_data['translator']

    operation_type = dialog_manager.dialog_data.get('operation')
    id: int = dialog_manager.dialog_data.get('user_id')
    currency: Currency = dialog_manager.dialog_data.get('currency')
    user: User | None = await db.user.get_by_where(
        whereclause=generate_user_whereclause(id),
        options=selectinload(User.wallet.and_(Wallet.currency == currency))
    )
    match operation_type:
        case 'refill':
            await db.refill.new(
                user_id_fk=user.id,
                wallet_id_fk=user.wallet[0].id,
                amount=amount,
                currency=currency,
                status=RefillStatus.SUCCESS,
                cause=RefillCause.GIFT,
            )
            user.wallet[0].balance += amount
        case 'withdraw':
            await db.withdraw.new(
                user_id_fk=user.id,
                wallet_id_fk=user.wallet[0].id,
                amount=amount,
                status=WithdrawStatus.SUCCESS,
                cause=WithdrawCause.ADMINS_DECISION
            )
            user.wallet[0].balance -= amount
    with suppress(TelegramBadRequest):
        await bot.send_message(
            chat_id=user.user_id,
            text=translator.get(
                f'input-amount-change-balance.notify-{operation_type}',
                amount=str(amount),
                currency=currency
            )
        )
    await db.session.commit()
    await dialog_manager.switch_to(
        CommonFunctionsState.user_profile
    )


@inject
async def on_input_message(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        message: str,
        db: FromDishka[Database],
        t_hub: FromDishka[Translator]
):
    bot, translator = dialog_manager.middleware_data['bot'], dialog_manager.middleware_data['translator']
    id: int = dialog_manager.dialog_data.get('user_id')
    user = await db.user.get_by_where(whereclause=generate_user_whereclause(id))

    try:
        user_t_runner = t_hub.t_hub.get_translator_by_locale(locale=user.lang)
        await bot.send_message(
            chat_id=user.user_id,
            text=user_t_runner.get(
                'input-message.notify-user',
                msg=message
            )
        )
        await event.reply(
            text=translator.get('input-message.notify-admin-success')
        )
    except TelegramBadRequest:
        await event.reply(
            text=translator.get('input-message.notify-admin-fail')
        )
    await dialog_manager.switch_to(CommonFunctionsState.user_profile)


def is_msg_with_media(msg: Message, media_helper: MediaHelper) -> bool:
    try:
        helper = media_helper.get_event(msg)
        if helper is not None:
            return True
    except KeyError:
        return False
    return False


@inject
async def on_mailing(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        media_helper: FromDishka[MediaHelper]
):
    if is_msg_with_media(event, media_helper):
        helper = media_helper.get_event(event)
        dialog_manager.dialog_data.update(
            {
                'file_id': (await helper.obtain_media(event)).file_id,
                'content_type': helper.content_type
            }
        )
    dialog_manager.dialog_data.update(
        {
            'ru_caption': event.caption if event.caption else event.text
        }
    )
    await dialog_manager.switch_to(CommonFunctionsState.mailing_en)


async def on_mailing_en(
        event: Message,
        widget: ManagedTextInput,
        dialog_manger: DialogManager,
        msg: str
):
    dialog_manger.dialog_data.update(
        {
            'en_caption': event.text
        }
    )
    return await dialog_manger.switch_to(
        CommonFunctionsState.mailing_approve
    )


@inject
async def on_approve(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        cache: FromDishka[Cache]
):
    bot: Bot = dialog_manager.middleware_data['bot']
    translator = dialog_manager.middleware_data['translator']
    await asyncio.create_task(
        mailing(
            admin_user_id=event.from_user.id,
            bot=bot,
            data=dialog_manager.dialog_data,
            db=db,
            cache=cache,
            translator=translator
        )
    )


async def mailing(
        admin_user_id: int,
        bot: Bot,
        data: dict,
        db: Database,
        cache: Cache,
        translator: TranslatorRunner,
):
    if data.get('file_id') is not None:
        return await media_mailing(admin_user_id, bot, data, db, cache, translator)
    await regular_mailing(admin_user_id, bot, data, db, cache, translator)


async def media_mailing(
        admin_user_id: int,
        bot: Bot,
        data: dict,
        db: Database,
        cache: Cache,
        translator: TranslatorRunner,
):
    content_type: ContentType = data.get('content_type')
    file_id: str = data.get('file_id')
    success_msg, error_msg = 0, 0
    ru_text, en_text = data.get('ru_caption'), data.get('en_caption')
    users_list = await db.user.get_many(whereclause=User.is_active == True, limit=1000000)
    start_msg = await bot.send_message(
        chat_id=admin_user_id,
        text=translator.get(
            'mailing-start',
            sent_messages=success_msg + error_msg,
            users_count=len(users_list)
        )
    )
    for user in users_list:
        try:
            method = getattr(bot, f'send_{content_type.lower()}')
            data = {
                'chat_id': user.user_id,
                content_type.lower(): file_id,
                'caption': en_text if user.lang == "EN" and en_text else ru_text
            }
            await method(
                **data
            )
            success_msg += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except TelegramBadRequest:
            error_msg += 1
            user.is_active = False
            redis_user = await cache.user.get_by_key(f'user:{user.user_id}')
            redis_user.is_active = False
            await cache.user.update_model(redis_user, f'{user.user_id}')
        if success_msg + error_msg % 10 == 0:
            await start_msg.edit_text(
                text=translator.get(
                    'mailing-start',
                    sent_messages=success_msg + error_msg,
                    users_count=len(users_list)
                )
            )
        await asyncio.sleep(0.08)
    await start_msg.edit_text(
        text=translator.get(
            'mailing-start.done',
            users_count=len(users_list),
            success_msg=success_msg,
            error_msg=error_msg
        )
    )


async def regular_mailing(
        admin_user_id: int,
        bot: Bot,
        data: dict,
        db: Database,
        cache: Cache,
        translator: TranslatorRunner,
):
    success_msg, error_msg = 0, 0
    ru_text, en_text = data.get('ru_caption'), data.get('en_caption')
    users_list = await db.user.get_many(whereclause=User.is_active == True, limit=1000000)
    start_msg = await bot.send_message(
        chat_id=admin_user_id,
        text=translator.get(
            'mailing-start',
            sent_messages=success_msg + error_msg,
            users_count=len(users_list)
        )
    )
    for user in users_list:
        try:
            await bot.send_message(
                chat_id=user.user_id,
                text=en_text if user.lang == "EN" and en_text else ru_text
            )
            success_msg += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except (TelegramBadRequest, TelegramForbiddenError):
            error_msg += 1
            user.is_active = False
            redis_user = await cache.user.get_by_key(f'user:{user.user_id}')
            redis_user.is_active = False
            await cache.user.update_model(redis_user, f'{user.user_id}')
        if success_msg + error_msg % 10 == 0:
            await start_msg.edit_text(
                text=translator.get(
                    'mailing-start',
                    sent_messages=success_msg + error_msg,
                    users_count=len(users_list)
                )
            )
        await asyncio.sleep(0.08)
    await start_msg.edit_text(
        text=translator.get(
            'mailing-start.done',
            users_count=len(users_list),
            success_msg=success_msg,
            error_msg=error_msg
        )
    )

    await db.session.commit()
