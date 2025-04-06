import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from src.bot.handlers.start_handlers import main_start
from src.cache.models import RedisUser, BotSettings


async def on_error(
        event: ErrorEvent,
        dialog_manager: DialogManager,
        translator: TranslatorRunner,
        redis_user: RedisUser,
        bot_settings: BotSettings
):
    logging.exception("Restarting bot: %s", event.exception)

    if event.update.callback_query:
        await event.update.callback_query.message.answer(
            text=translator.get('errors.unexpected-error-msg')
        )
        message_event = event.update.callback_query.message
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    elif event.update.message:
        await event.update.message.answer(
            text=translator.get('errors.unexpected-error-msg'),
            reply_markup=ReplyKeyboardRemove(),
        )
        message_event = event.update.message
    return await main_start(
        message_event,
        dialog_manager,
        translator,
        redis_user,
        bot_settings
    )
