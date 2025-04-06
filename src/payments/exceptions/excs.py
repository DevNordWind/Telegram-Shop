from src.payments.enums import PaymentMethod


class FailOrderCreate(Exception):
    pass


class WrongMinAmount(Exception):
    def __init__(self, min_amount: float | int):
        self.min_amount = min_amount
        super().__init__(f"Min Amount is {self.min_amount}")


class BadRequest(Exception):
    def __init__(self, payment_method: PaymentMethod, code: int, message: str) -> None:
        self.payment_method = payment_method
        self.code = code
        self.message = message
        super().__init__(f"PaymentSystem: {payment_method.name} returns code {code} with \"{message}\"")
