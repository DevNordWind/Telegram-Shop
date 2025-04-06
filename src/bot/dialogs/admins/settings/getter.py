from aiogram.types import User
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.utilities import MediaHelper
from src.bot.utilities.media_helper.exceptions import NeedUpdate
from src.bot.utilities.misc import render_settings_text
from src.cache import Cache
from src.cache.models import BotSettings, RedisUser
from src.db.enums import Lang


async def change_data_getter(dialog_manager: DialogManager, **kwargs):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    return {
        **bot_settings.__dict__
    }


async def input_start_text_ru_getter(dialog_manager: DialogManager, **kwargs):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    return {
        **bot_settings.__dict__
    }


@inject
async def current_msg_getter(dialog_manager: DialogManager, media_helper: FromDishka[MediaHelper],
                             cache: FromDishka[Cache], **kwargs) -> dict:
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    user: User = dialog_manager.middleware_data['event_context'].user
    translator: TranslatorRunner = dialog_manager.middleware_data.get('translator')
    current_msg = render_settings_text(
        user,
        translator,
        text=bot_settings.start_text_ru if redis_user.lang == Lang.RU else bot_settings.start_text_en
    )

    dict_to_return = {
        'current_msg': current_msg
    }

    if bot_settings.start_media_path and bot_settings.start_media_id and bot_settings.start_media_content_type:
        helper = media_helper.get(bot_settings.start_media_content_type)
        try:
            media = await helper.get_media_attachment(
                chat_id=dialog_manager.event.from_user.id,
                file_id=bot_settings.start_media_id,
                file_path=bot_settings.start_media_path,
            )
        except NeedUpdate as e:
            bot_settings.start_media_id = e.media_id
            await cache.bot_settings.update_model(bot_settings)
            media = e.media_attachment
        dict_to_return.update(
            {
                'media': media
            }
        )
    return dict_to_return


async def input_faq_text_ru_getter(dialog_manager: DialogManager, **kwargs):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    return {
        **bot_settings.__dict__
    }


async def current_faq_msg_getter(dialog_manager: DialogManager, **kwargs):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    user: User = dialog_manager.middleware_data['event_context'].user
    translator: TranslatorRunner = dialog_manager.middleware_data.get('translator')
    current_msg = render_settings_text(
        user=user,
        translator=translator,
        text=bot_settings.faq_text_ru if redis_user.lang == Lang.RU else bot_settings.faq_text_en
    )
    dict_to_return = {
        'current_msg': current_msg
    }
    return dict_to_return

async def switches_getter(dialog_manager: DialogManager, **kwargs):
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    return {
        **bot_settings.__dict__
    }