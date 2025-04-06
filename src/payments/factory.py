from aiocryptopay import AioCryptoPay

from .enums import PaymentMethod
from .managers import *


class PaymentCreator:

    def __init__(self, aiocryptopay: AioCryptoPay):
        self.aiocryptopay = aiocryptopay

    async def get(self, key: PaymentMethod) -> PaymentManager:
        managers_dict = {
            PaymentMethod.CRYPTOBOT: CbManager(
                aiocryptopy=self.aiocryptopay
            ),
        }
        try:
            return managers_dict[key]
        except KeyError:
            raise ValueError("Wrong type of PaymentMethods")
