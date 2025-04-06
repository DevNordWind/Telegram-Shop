from dataclasses import dataclass
from decimal import Decimal

from src.db.enums import Currency
from src.payments.enums import PaymentMethod


@dataclass
class InvoiceData:
    id: str
    amount: Decimal
    currency: Currency
    payment_method: PaymentMethod


@dataclass
class Invoice:
    id: str
    amount: Decimal
    pay_url: str
    currency: Currency
    payment_method: PaymentMethod
    external_id: str | None = None
