from aiocryptopay.const import InvoiceStatus
from aiocryptopay.models.invoice import Invoice
from aiocryptopay.models.update import Update
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from src.bot.interactors import PaymentInteractor
from src.configuration import conf
from src.payments import PaymentCreator
from src.payments.enums import PaymentMethod
from src.payments.managers import CbManager

payment_router = APIRouter()


@payment_router.post(path=conf.webhook.cb_path)
@inject
async def check_invoice_cb(request: Request, pay_creator: FromDishka[PaymentCreator],
                           pay_interactor: FromDishka[PaymentInteractor]):
    body = await request.json()
    body_text = await request.body()
    crypto_pay_signature = request.headers.get(
        "Crypto-Pay-Api-Signature", "No value"
    )
    cb_manager: CbManager = await pay_creator.get(PaymentMethod.CRYPTOBOT)
    signature = cb_manager.check_signature(
        body_text=str(body_text, encoding='utf-8'), crypto_pay_signature=crypto_pay_signature
    )
    if signature:
        payload: Invoice = Update(**body).payload
        if payload.status == InvoiceStatus.PAID:
            await pay_interactor.give_award(refill_id=payload.payload)
        return Response(status_code=200)
