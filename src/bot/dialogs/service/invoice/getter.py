from adaptix import Retort
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.payments.models import Invoice


@inject
async def invoice_getter(dialog_manager: DialogManager, retort: FromDishka[Retort], **kwargs):
    invoice: Invoice = retort.load(dialog_manager.start_data, Invoice)
    return {
        'amount': str(invoice.amount),
        'currency': invoice.currency.name,
        'payment_method': invoice.payment_method.value,
        'pay_url': invoice.pay_url
    }
