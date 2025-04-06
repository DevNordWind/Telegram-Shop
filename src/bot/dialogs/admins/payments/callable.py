from contextlib import suppress
from typing import Any

from aiocryptopay import AioCryptoPay
from aiocryptopay.exceptions import CryptoPayAPIError, CodeErrorFactory
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from pydantic import ValidationError

from src.bot.interactors import PaymentInteractor
from src.bot.states import PaymentManagementState
from src.cache import Cache
from src.cache.models import BotSettings
from src.db import Database
from src.db.models import Refill


@inject
async def on_cb_switch(event: CallbackQuery, widget: Button, dialog_manager: DialogManager, cache: FromDishka[Cache], cb: FromDishka[AioCryptoPay]):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    try:
        await cb.get_me()
        bot_settings.status_cryptobot = not bot_settings.status_cryptobot
    except CodeErrorFactory as e:
        if e.code == 401:
            bot_settings.status_cryptobot = False
            await event.answer(
                text=translator.get('cb-fail')
            )
    await cache.bot_settings.update_model(bot_settings)


@inject
async def on_steam_switch(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        cache: FromDishka[Cache]
):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    bot_settings.status_steam = not bot_settings.status_steam
    await cache.bot_settings.update_model(bot_settings)

