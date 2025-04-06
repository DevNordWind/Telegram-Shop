import abc
from abc import ABC
from contextlib import suppress
from typing import BinaryIO

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, File, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from aiogram_dialog.api.entities import MediaAttachment


class AbstractMediaHelper(ABC):
    bot: Bot
    content_type: ContentType | None = None

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    async def is_media_valid(self, file_id: str) -> bool:
        with suppress(TelegramBadRequest):
            await self.bot.get_file(file_id)
            return True
        return False

    @abc.abstractmethod
    async def obtain_media(self, event: Message) -> File:
        raise NotImplementedError

    @abc.abstractmethod
    async def send_media(self,
                         chat_id: str | int,
                         file_id: str,
                         file_path: str,
                         caption: str | None = None,
                         reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None
                         ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_media_attachment(self,
                                   chat_id: str | int,
                                   file_id: str,
                                   file_path: str,
                                   caption: str | None = None,
                                   ) -> MediaAttachment:
        raise NotImplementedError


    @abc.abstractmethod
    async def download_media(self,
                             file_id: str,
                             destination: str
                             ) -> BinaryIO:
        raise NotImplementedError
