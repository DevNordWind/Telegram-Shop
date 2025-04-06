from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message

from .managers import *


class MediaHelper:
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    def get(self, content_type: ContentType) -> AbstractMediaHelper:
        return {
            ContentType.PHOTO: PhotoHelper(self.bot),
            ContentType.VIDEO: VideoHelper(self.bot),
            ContentType.ANIMATION: AnimationHelper(self.bot),
        }[content_type]

    def get_event(self, event: Message) -> AbstractMediaHelper:
        media_handlers = {
            "photo": PhotoHelper,
            "video": VideoHelper,
            'animation': AnimationHelper,
        }
        # Найдем первый существующий атрибут
        media_type = next((key for key in media_handlers if getattr(event, key)), None)

        if media_type:
            return media_handlers[media_type](self.bot)
