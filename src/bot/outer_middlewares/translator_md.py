from collections.abc import Awaitable, Callable
from typing import Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, ErrorEvent, User
from dishka.integrations.aiogram import CONTAINER_NAME

from src.translator import Translator


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery | ErrorEvent,
            data: Dict
    ) -> Any:
        redis_user = data['redis_user']
        aio_user: User = data['event_context'].user
        translator: Translator = await data[CONTAINER_NAME].get(Translator)
        data['translator'] = translator.t_hub.get_translator_by_locale(
            locale=redis_user.lang if redis_user and redis_user.lang else aio_user.language_code.upper()
        )
        return await handler(event, data)
