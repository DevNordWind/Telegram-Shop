from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.bot.handlers.start_handlers import main_start
from src.cache import Cache
from src.db import Database
from src.db.enums import Lang
from src.db.models import User
from src.translator import Translator


@inject
async def on_lang_select(
        event: CallbackQuery,
        widget: Any,
        dialog_manager: DialogManager,
        item_id: str,
        db: FromDishka[Database],
        cache: FromDishka[Cache],
        translator: FromDishka[Translator]
):
    lang = Lang(item_id)
    redis_user, bot_settings = dialog_manager.middleware_data['redis_user'], dialog_manager.middleware_data[
        'bot_settings']
    redis_user.lang = lang
    await db.user.update(User.id == redis_user.id, values={'lang': lang})
    await cache.user.update_model(redis_user, f'{event.from_user.id}')
    await db.session.commit()

    await dialog_manager.done()
    await event.message.delete()

    return await main_start(
        event=event.message,
        translator=translator.t_hub.get_translator_by_locale(locale=item_id),
        redis_user=redis_user,
        bot_settings=bot_settings,
        dialog_manager=dialog_manager,
    )
