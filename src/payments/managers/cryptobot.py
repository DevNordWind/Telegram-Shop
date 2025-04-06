import logging
from hashlib import sha256
from hmac import HMAC

from aiocryptopay import AioCryptoPay
from aiocryptopay.const import InvoiceStatus
from aiocryptopay.exceptions import CodeErrorFactory
from aiocryptopay.models.invoice import Invoice as CryptoInvoice
from aiocryptopay.models.profile import Profile

from .abstract import PaymentManager
from ..enums import PaymentMethod
from ..exceptions import FailOrderCreate, WrongMinAmount
from ..models import InvoiceData, Invoice
from ...configuration import conf


class CbManager(PaymentManager):
    def __init__(self, aiocryptopy: AioCryptoPay):
        super().__init__()
        self.cb: AioCryptoPay = aiocryptopy
        self.__token = conf.cb.token
        self.payment_method = PaymentMethod.CRYPTOBOT

    async def is_available(self) -> bool:
        try:
            return isinstance(await self.cb.get_me(), Profile)
        except CodeErrorFactory as e:
            logging.error(e.name)
            return False

    async def create_invoice(self, invoice_data: InvoiceData) -> Invoice:
        crypto_invoice = await self.__generate_invoice(invoice_data)
        return Invoice(
            id=invoice_data.id,
            amount=invoice_data.amount,
            currency=invoice_data.currency,
            pay_url=crypto_invoice.bot_invoice_url,
            external_id=str(crypto_invoice.invoice_id),
            payment_method=self.payment_method
        )

    async def __generate_invoice(self, invoice_data: InvoiceData):
        try:
            return await self.cb.create_invoice(
                amount=invoice_data.amount,
                fiat=invoice_data.currency.name,
                currency_type='fiat',
                expires_in=10800,
                payload=invoice_data.id
            )
        except CodeErrorFactory as e:
            if e.name == "AMOUNT_TOO_SMALL":
                raise WrongMinAmount
            raise FailOrderCreate

    def check_signature(self, body_text: str, crypto_pay_signature: str) -> bool:
        """
        https://help.crypt.bot/crypto-pay-api#verifying-webhook-updates

        Args:
            body_text (str): webhook update body
            crypto_pay_signature (str): Crypto-Pay-Api-Signature header

        Returns:
            bool: is cryptopay api signature
        """
        token = sha256(string=self.__token.encode("UTF-8")).digest()
        signature = HMAC(
            key=token, msg=body_text.encode("UTF-8"), digestmod=sha256
        ).hexdigest()
        return signature == crypto_pay_signature

    async def check_invoice(self, invoice: Invoice) -> bool:
        crypto_invoice: CryptoInvoice = await self.cb.get_invoices(
            invoice_ids=invoice.external_id,
        )
        return crypto_invoice[0].status == InvoiceStatus.PAID
