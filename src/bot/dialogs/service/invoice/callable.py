from typing import Any

from adaptix import Retort
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.interactors import PaymentInteractor
from src.db import Database
from src.payments import PaymentCreator
from src.payments.models import Invoice


@inject
async def on_success(
        event: Message,
        widget: Any,
        dialog_manager: DialogManager,
        item_id: str,
        **kwargs
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    return await event.reply(
        text=translator.get('errors.unauthorized-closing-msg')
    )


@inject
async def on_error(
        event: Message,
        widget: Any,
        dialog_manager: DialogManager,
        error: ValueError,
        **kwargs
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    return await event.reply(
        text=translator.get('errors.unauthorized-closing-msg')
    )


async def on_close(event: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await event.message.delete()


@inject
async def on_check_invoice(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        payment_creator: FromDishka[PaymentCreator],
        payment_interactor: FromDishka[PaymentInteractor],
        retort: FromDishka[Retort],
):
    invoice: Invoice = retort.load(dialog_manager.start_data, Invoice)
    payment_mg = await payment_creator.get(invoice.payment_method)
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    if await payment_mg.check_invoice(invoice):
        await payment_interactor.on_payment_notification(refill_id=invoice.id)
        return await dialog_manager.done()
    await event.answer(translator.get('invoice.payment-not-found'))
