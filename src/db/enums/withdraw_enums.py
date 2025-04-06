import enum


class WithdrawCause(str, enum.Enum):
    ADMINS_DECISION = "ADMINS_DECISION"

class WithdrawStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"
