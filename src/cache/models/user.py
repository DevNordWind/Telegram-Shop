from dataclasses import dataclass

from src.db.enums import Currency, Lang, Role


@dataclass
class RedisUser:
    id: int  # It's mean internal id from database
    first_name: str
    currency: Currency
    role: Role
    lang: Lang | None = None
    username: str | None = None
    last_name: str | None = None
    is_active: bool = True
    @staticmethod
    def build_key(user_id: int | str) -> str:
        return f"user:{user_id}"
