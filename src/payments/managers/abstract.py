from abc import ABC, abstractmethod

from ..models import InvoiceData, Invoice


class PaymentManager(ABC):

    @abstractmethod
    async def create_invoice(self, invoice_data: InvoiceData) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    async def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def check_invoice(self, invoice: Invoice) -> bool:
        raise NotImplementedError