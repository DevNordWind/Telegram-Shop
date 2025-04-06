from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import CONTAINER_NAME
from fluentogram import TranslatorRunner

from src.bot.filters import TranslatorFilter, IsAdminFilter
from src.bot.kbs import menu_frep
from src.bot.states import ProfileState, FaqState, SupportState, ShoppingState
from src.bot.utilities import MediaHelper
from src.bot.utilities.media_helper.exceptions import NeedUpdate
from src.bot.utilities.misc import render_settings_text
from src.cache import Cache
from src.cache.models import RedisUser, BotSettings
from src.db.enums import Role, Lang
from ..kbs import admin_products_kb, admin_settings_kb, admin_common_functions_kb, admin_payments_kb
from ..states import CategoryManagementState, PositionManagementState, DeleteProductsState, ItemManagementState, \
    SettingsState, CommonFunctionsState, PaymentManagementState, StatisticState

start_router = Router()


async def attempt_media_answer(
        event: Message,
        dialog_manager: DialogManager,
        translator: TranslatorRunner,
        bot_settings: BotSettings,
        redis_user: RedisUser,
        text: str
):
    async_container = dialog_manager.middleware_data[CONTAINER_NAME]
    cache = await async_container.get(Cache)
    helper = (await async_container.get(MediaHelper)).get(bot_settings.start_media_content_type)

    try:
        return await helper.send_media(
            chat_id=event.chat.id,
            file_id=bot_settings.start_media_id,
            file_path=bot_settings.start_media_path,
            caption=text,
            reply_markup=menu_frep(
                is_admin=redis_user.role == Role.ADMINISTRATOR,
                translator=translator
            )
        )
    except NeedUpdate as e:
        bot_settings.start_media_id = e.media_id
        return await cache.bot_settings.update_model(bot_settings, 'settings')


async def attempt_find_text(
        user: User,
        bot_settings: BotSettings,
        lang: Lang,
        translator: TranslatorRunner
) -> str:
    if bot_settings.start_text_ru and bot_settings.start_text_en:
        text = bot_settings.start_text_ru if lang == Lang.RU else bot_settings.start_text_en
        return render_settings_text(user, translator, text)
    return translator.get('main')


@start_router.message(CommandStart())
async def main_start(
        event: Message,
        dialog_manager: DialogManager,
        translator: TranslatorRunner,
        redis_user: RedisUser,
        bot_settings: BotSettings,
):
    text = await attempt_find_text(
        user=event.from_user,
        bot_settings=bot_settings,
        lang=redis_user.lang,
        translator=translator
    )
    if (bot_settings.start_media_path is not None and
            bot_settings.start_media_id is not None and
            bot_settings.start_media_content_type is not None):
        return await attempt_media_answer(
            event=event,
            dialog_manager=dialog_manager,
            translator=translator,
            redis_user=redis_user,
            bot_settings=bot_settings,
            text=text
        )
    return await event.answer(
        text=text,
        reply_markup=menu_frep(
            is_admin=redis_user.role == Role.ADMINISTRATOR,
            translator=translator
        )
    )


@start_router.message(TranslatorFilter('main.profile-btn'))
async def start_profile(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        ProfileState.profile, mode=StartMode.RESET_STACK
    )


@start_router.message(TranslatorFilter('main.faq-btn'))
async def start_faq(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        FaqState.faq, mode=StartMode.RESET_STACK
    )


@start_router.message(TranslatorFilter('main.support-btn'))
async def start_support(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        SupportState.support, mode=StartMode.RESET_STACK
    )


@start_router.message(TranslatorFilter('main.buy-btn'))
async def start_shopping(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        ShoppingState.select_category, mode=StartMode.RESET_STACK
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('main.item-management-btn'))
async def start_product_management(event: Message, translator: TranslatorRunner):
    return await event.answer(
        text=translator.get('product-management'),
        reply_markup=admin_products_kb(translator)
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('main.settings-btn'))
async def start_settings(event: Message, translator: TranslatorRunner):
    return await event.answer(
        text=translator.get('admin-settings'),
        reply_markup=admin_settings_kb(translator)
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('admin-settings.change-data-btn'))
async def start_change_data(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=SettingsState.change_data
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('product-management.create-category-btn'))
async def start_add_category(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=CategoryManagementState.input_category_name_ru
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('product-management.edit-category-btn'))
async def start_edit_category(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=CategoryManagementState.categories_list
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('product-management.deleting-btn'))
async def start_delete(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=DeleteProductsState.delete
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('product-management.create-position-btn'))
async def start_add_position(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=PositionManagementState.select_category_add_position
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('product-management.edit-position-btn'))
async def start_edit_position(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=PositionManagementState.select_category_edit_position
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('product-management.add-item-btn'))
async def start_add_items(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=ItemManagementState.select_category_add_items
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('admin-settings.switches-btn'))
async def start_switches(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=SettingsState.switches
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('main.common-functions-btn'))
async def start_common_functions(event: Message, translator: TranslatorRunner):
    return await event.answer(
        text=translator.get('common-functions'),
        reply_markup=admin_common_functions_kb(translator)
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('common-functions.find-btn'))
async def start_find(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=CommonFunctionsState.find
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('common-functions.mailing-btn'))
async def start_mailing(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=CommonFunctionsState.mailing
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('main.payment-systems-btn'))
async def start_payment(event: Message, translator: TranslatorRunner):
    return await event.answer(
        text=translator.get('payment'),
        reply_markup=admin_payments_kb(translator)
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('payment.cb-btn'))
async def start_cb(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=PaymentManagementState.cryptobot
    )


@start_router.message(IsAdminFilter(), TranslatorFilter('main.statistic-btn'))
async def start_statistic(event: Message, dialog_manager: DialogManager):
    return await dialog_manager.start(
        mode=StartMode.RESET_STACK,
        state=StatisticState.statistic
    )
