"""This file represents configurations from files and environment."""
import enum
import logging
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from os import getenv

import colorlog
from aiocryptopay import Networks
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


class DatabaseType(str, enum.Enum):
    POSTGRES = "POSTGRES"
    SQLITE3 = "SQLITE3"


@dataclass
class DataStorage:
    position_media_path: str = getenv("POSITIONS_MEDIA_PATH", "./data/positions")
    start_media_path: str = getenv("START_MEDIA_PATH", "./data/start")
    db_path: str = getenv("DB_PATH", './data/db')


class DatabaseType(str, enum.Enum):
    POSTGRES = "POSTGRES"
    SQLITE3 = "SQLITE3"


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    db_type: DatabaseType = getenv("DB_TYPE", DatabaseType.SQLITE3)
    name: str = getenv('DB_NAME', "db")
    user: str | None = getenv('DB_USER')
    password: str | None = getenv("DB_PASSWORD")
    host: str | None = getenv('DB_HOST')
    port: int | None = int(getenv("DB_PORT"))

    def build_connection_str(self) -> str:
        """This function build a connection string."""
        data = {
            DatabaseType.SQLITE3: self.__generate_sqllite_connection,
            DatabaseType.POSTGRES: self.__generate_postgres_connection
        }
        return data[self.db_type]()

    def __generate_postgres_connection(self) -> str:
        driver: str = 'asyncpg'
        database_system: str = 'postgresql'
        return URL.create(
            drivername=f'{database_system}+{driver}',
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)

    def __generate_sqllite_connection(self) -> str:
        database_system: str = 'sqlite'
        driver: str = 'aiosqlite'
        return URL.create(
            drivername=f'{database_system}+{driver}',
            database=f'./data/db/{self.name}.db'
        ).render_as_string(hide_password=False)


@dataclass
class CryptoBotConfig:
    token: str | None = getenv("CB_TOKEN")
    network: Networks | None = Networks.TEST_NET if getenv('TEST_NETWORK') == '1' else Networks.MAIN_NET


@dataclass
class RedisConfig:
    """Redis connection variables."""

    db: int = int(getenv('REDIS_DATABASE', 1))
    """ Redis Database ID """
    host: str = getenv('REDIS_HOST', 'redis')
    port: int = int(getenv('REDIS_PORT', 6379))
    passwd: str | None = getenv('REDIS_PASSWORD')
    username: str | None = getenv('REDIS_USERNAME')
    state_ttl: int | None = getenv('REDIS_TTL_STATE', None)
    data_ttl: int | None = getenv('REDIS_TTL_DATA', None)


@dataclass
class BotConfig:
    """Bot configuration."""

    token: str | None = getenv('BOT_TOKEN', None)


@dataclass
class WebhookConfig:
    webhook_mode: bool = bool(int(getenv("WEBHOOK_MODE", '0')))
    base_url: str | None = getenv("WEBHOOK_BASE_URL")
    cb_path: str = getenv("CB_PATH", '/cryptobot')


@dataclass
class Logging:
    _logging_level: int = int(getenv("LOGGING_LEVEL", default=20))
    _path_log = './data/logs/logs.log'
    _format_file = "%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s"
    _format_stdout = colorlog.ColoredFormatter(
        "%(purple)s%(levelname)s %(blue)s|%(purple)s %(asctime)s %(blue)s|%(purple)s %(filename)s:%(lineno)d %(blue)s|%(purple)s %(message)s%(red)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    @property
    def is_debug(self) -> bool:
        return self._logging_level == logging.DEBUG

    def setup_logger(self) -> logging.getLogger:
        logger = logging.getLogger()
        logger.setLevel(self._logging_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._logging_level)
        console_handler.setFormatter(colorlog.ColoredFormatter(
            "%(purple)s%(levelname)s %(blue)s|%(purple)s %(asctime)s %(blue)s|%(purple)s %(filename)s:%(lineno)d %(blue)s|%(purple)s %(message)s%(red)s",
            datefmt="%d-%m-%Y %H:%M:%S",
        ))

        file_handler = RotatingFileHandler(self._path_log, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.WARNING)

        formatter = logging.Formatter(self._format_file)
        console_handler.setFormatter(self._format_stdout)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


@dataclass
class AdminsConfig:
    admins: str = getenv("ADMINS", '')

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.get_admins()

    def get_admins(self) -> list[int]:
        admins = self.admins
        if ',' in admins:
            return [int(admin.strip()) for admin in admins.split(',')]
        return [int(admins.strip())]


@dataclass
class Configuration:
    """All in one configuration's class."""
    data = DataStorage()
    log = Logging()
    db = DatabaseConfig()
    redis = RedisConfig()
    bot = BotConfig()
    webhook = WebhookConfig()
    cb = CryptoBotConfig()
    admin = AdminsConfig()


conf = Configuration()
