import enum


class Currency(str, enum.Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
    UAH = "UAH"

