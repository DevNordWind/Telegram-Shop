import enum


class Lang(str, enum.Enum):
    RU = "RU"
    EN = "EN"


class Role(str, enum.Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    USER = "USER"
