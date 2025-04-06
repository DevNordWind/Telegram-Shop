import logging
from typing import BinaryIO

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile, Message, File, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    ForceReply
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from .abstract import AbstractMediaHelper
from ..exceptions import NeedUpdate


class AnimationHelper(AbstractMediaHelper):
    content_type = ContentType.ANIMATION

    def __init__(self, bot: Bot):
        super().__init__(bot)

    async def obtain_media(self, event: Message) -> File:
        return await self.bot.get_file(file_id=event.animation.file_id)

    async def send_media(self,
                         chat_id: str | int,
                         file_id: str,
                         file_path: str,
                         caption: str | None = None,
                         reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None
                         ):
        try:
            await self.bot.send_animation(
                chat_id=chat_id,
                animation=file_id,
                caption=caption,
                reply_markup=reply_markup
            )
        except TelegramBadRequest as e:
            logging.error(e)
            msg = await self.bot.send_animation(
                chat_id=chat_id,
                animation=FSInputFile(file_path),
                caption=caption,
                reply_markup=reply_markup
            )
            raise NeedUpdate(
                media_id=msg.animation.file_id
            )

    async def download_media(self,
                             file_id: str,
                             destination: str
                             ) -> BinaryIO:
        return await self.bot.download(
            file_id,
            destination
        )

    async def get_media_attachment(self,
                                   chat_id: str | int,
                                   file_id: str,
                                   file_path: str,
                                   caption: str | None = None,
                                   ) -> MediaAttachment:
        if not await self.is_media_valid(file_id):
            if caption is None:
                caption = "Uploading an animation..."
            msg = await self.bot.send_animation(
                chat_id=chat_id,
                animation=FSInputFile(file_path),
                caption=caption
            )
            try:
                media_id = (await self.obtain_media(msg)).file_id
                raise NeedUpdate(
                    media_id=media_id,
                    media_attachment=MediaAttachment(
                        type=self.content_type,
                        file_id=MediaId(media_id)
                    )
                )
            finally:
                await msg.delete()
        return MediaAttachment(
            type=self.content_type,
            file_id=MediaId(file_id)
        )
