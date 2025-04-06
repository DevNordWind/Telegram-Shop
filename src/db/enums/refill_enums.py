import enum


class RefillStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"

class RefillCause(str, enum.Enum):
    PAYMENT = 'PAYMENT'
    GIFT = 'GIFT'