from aiogram import Router, Bot
from aiogram.types import TelegramObject, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.entities import EventContext
from fluentogram import TranslatorRunner

from src.bot.kbs import tech_work_support_kb
from src.bot.states import SelectLangState
from src.cache.models import RedisUser, BotSettings
from .start_handlers import main_start
from ..filters import IsWorkFilter, IsSelectLangFilter, TranslatorFilter

service_router = Router()


@service_router.message(IsWorkFilter())
@service_router.callback_query(IsWorkFilter())
async def on_work(
        event: TelegramObject,
        bot: Bot,
        translator: TranslatorRunner,
        bot_settings: BotSettings,
        event_context: EventContext
):
    if bot_settings.support:
        reply_markup = tech_work_support_kb(translator, bot_settings.support)
    else:
        reply_markup = None
    return await bot.send_message(
        chat_id=event_context.user.id,
        text=translator.get('tech-work'),
        reply_markup=reply_markup
    )


@service_router.message(IsSelectLangFilter())
@service_router.callback_query(IsSelectLangFilter())
async def start_select_language(event: TelegramObject, dialog_manager: DialogManager):
    return await dialog_manager.start(
        SelectLangState.select_lang, mode=StartMode.RESET_STACK
    )


@service_router.message(TranslatorFilter('back'))
async def back_to_main(
        event: Message,
        dialog_manager: DialogManager,
        translator: TranslatorRunner,
        redis_user: RedisUser,
        bot_settings: BotSettings,
):
    return await main_start(
        event,
        dialog_manager,
        translator,
        redis_user,
        bot_settings,
    )
