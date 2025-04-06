import uuid
from decimal import Decimal
from typing import Any

from adaptix import Retort
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.states.user_states import RefillState, InvoiceState
from src.cache.models import RedisUser
from src.db import Database
from src.db.models import Refill, Wallet
from src.payments import PaymentCreator
from src.payments.enums import PaymentMethod
from src.payments.exceptions import FailOrderCreate, WrongMinAmount
from src.payments.models import InvoiceData


@inject
async def on_refill_input_success(event: Message, widget: Any, dialog_manager: DialogManager, amount):
    dialog_manager.dialog_data.update(
        {
            'amount': str(amount)
        }
    )
    await dialog_manager.switch_to(
        RefillState.select_payment_method
    )


async def on_refill_input_error(event: Message, widget: Any, dialog_manager: DialogManager, error: ValueError):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    return await event.reply(
        translator.get('errors.invalid-number-msg')
    )


@inject
async def on_select_payment_method(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        pay_creator: FromDishka[PaymentCreator],
        db: FromDishka[Database],
        retort: FromDishka[Retort]
):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    payment_method = PaymentMethod(widget.widget_id)

    invoice_data = InvoiceData(
        payment_method=payment_method,
        amount=Decimal(dialog_manager.dialog_data['amount']),
        currency=redis_user.currency,
        id=str(uuid.uuid4())
    )

    try:
        pay_mg = await pay_creator.get(payment_method)
        invoice = await pay_mg.create_invoice(invoice_data)
        wallet = await db.wallet.get_with_refill(
            whereclause=((Wallet.user_id_fk == redis_user.id) & (Wallet.currency == redis_user.currency)),
        )
        wallet.refill.append(
            Refill(
                id=invoice.id,
                user_id_fk=redis_user.id,
                external_id=invoice.external_id,
                amount=invoice.amount,
                currency=redis_user.currency,
                payment_method=payment_method
            )
        )
        await db.session.commit()
        return await dialog_manager.start(
            InvoiceState.invoice, mode=StartMode.RESET_STACK, data=retort.dump(invoice)
        )
    except FailOrderCreate:
        return await event.message.reply(
            text=translator.get(
                'errors.fail_order_create'
            )
        )
    except WrongMinAmount as e:
        return await event.message.reply(
            text=translator.get(
                'errors.wrong_min_amount',
                min_amount=e.min_amount,
                fiat=invoice_data.currency
            )
        )
