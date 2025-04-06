from typing import Any

from aiofiles import os
from aiogram.types import Message, File, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.states import SettingsState
from src.bot.utilities import MediaHelper
from src.bot.utilities.misc import is_html_valid, format_settings_text
from src.cache import Cache
from src.cache.models import BotSettings
from src.configuration import conf


async def on_start_message_input(event: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    if not await is_html_valid(event):
        return await event.reply(
            text=translator.get('errors.html-error-msg')
        )
    try:
        format_settings_text(
            user=event.from_user,
            text=text,
            null_username=translator.get('null-username')
        )
    except KeyError:
        return await event.reply(translator.get('errors.format-error'))

    dialog_manager.dialog_data.update(
        {
            f'start_text_{widget.widget_id}': text
        }
    )
    return await dialog_manager.next()


@inject
async def on_start_media(
        event: Message,
        widget: Any,
        dialog_manager: DialogManager,
        cache: FromDishka[Cache],
        media_helper: FromDishka[MediaHelper]
):
    helper = media_helper.get_event(event)
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']

    file: File = await helper.obtain_media(event)
    ext = file.file_path.split('.')[-1]
    if bot_settings.start_media_path:
        await os.remove(
            bot_settings.start_media_path
        )
    destination = f'{conf.data.start_media_path}/start_media.{ext}'
    await helper.download_media(file_id=file.file_id, destination=destination)
    dialog_manager.dialog_data.update(
        {
            'start_media_id': file.file_id,
            'start_media_path': destination,
            'start_media_content_type': helper.content_type
        }
    )
    await write_start_msg_changes(dialog_manager, cache)
    await dialog_manager.switch_to(SettingsState.change_data)


async def write_start_msg_changes(dialog_manager: DialogManager, cache: Cache):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    keys = ['start_text_ru', 'start_text_en', 'start_media_id', 'start_media_path', 'start_media_content_type']
    for key in keys:
        bot_settings.__dict__.update(
            {
                key: dialog_manager.dialog_data.get(key)
            }
        )
    await cache.bot_settings.update_model(bot_settings)


@inject
async def on_media_skip(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        cache: FromDishka[Cache]
):
    await write_start_msg_changes(dialog_manager, cache)
    await dialog_manager.switch_to(
        SettingsState.change_data
    )


async def on_input_faq_text_ru(event: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    if not await is_html_valid(event):
        return await event.reply(
            text=translator.get('errors.html-error-msg')
        )
    try:
        format_settings_text(
            user=event.from_user,
            text=text,
            null_username=translator.get('null-username')
        )
    except KeyError:
        return await event.reply(translator.get('errors.format-error'))
    dialog_manager.dialog_data.update(
        {
            'faq_text_ru': text
        }
    )
    await dialog_manager.switch_to(SettingsState.faq_text_en)


@inject
async def on_input_faq_text_en(event: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str,
                               cache: FromDishka[Cache]):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    if not await is_html_valid(event):
        return await event.reply(
            text=translator.get('errors.html-error-msg')
        )
    try:
        format_settings_text(
            user=event.from_user,
            text=text,
            null_username=translator.get('null-username')
        )
    except KeyError:
        return await event.reply(translator.get('errors.format-error'))
    bot_settings.faq_text_ru = dialog_manager.dialog_data.get('faq_text_ru')
    bot_settings.faq_text_en = text
    await cache.bot_settings.update_model(bot_settings)
    await dialog_manager.switch_to(SettingsState.change_data)


@inject
async def on_input_support(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str,
        cache: FromDishka[Cache]):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']

    if '@' in text:
        text = text.replace('@', '')

    bot_settings.support = text
    await cache.bot_settings.update_model(bot_settings)
    return await dialog_manager.switch_to(
        SettingsState.change_data
    )

@inject
async def on_switches(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        cache: FromDishka[Cache]
):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    bot_settings.__dict__.update(
        {
            widget.widget_id: not getattr(bot_settings, widget.widget_id)
        }
    )
    await cache.bot_settings.update_model(bot_settings)

