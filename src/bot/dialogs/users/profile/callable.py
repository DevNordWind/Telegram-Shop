import asyncio

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Select, Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.bot.kbs import menu_frep
from src.bot.states import ProfileState
from src.cache import Cache
from src.cache.models import RedisUser
from src.db import Database
from src.db.enums import Lang, Role, Currency
from src.db.models import User, Item
from src.translator import Translator


async def on_select_purchase(event: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(
        {
            'purchase_id': item_id
        }
    )
    return await dialog_manager.switch_to(
        ProfileState.purchase_details
    )

@inject
async def on_unload_items(event: CallbackQuery, widget: Button, dialog_manager: DialogManager, db: FromDishka[Database]):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    purchase_id_fk: str = str(dialog_manager.dialog_data.get('purchase_id'))
    items = await db.item.get_many(
        whereclause=Item.purchase_id_fk == purchase_id_fk,
        limit=99999,
        order_by=Item.id
    )

    items_list = [f'{i}. {items[i].content}' for i in range(0, len(items))]
    message = '\n\n'.join(items_list)
    msgs = [message[i:i + 4096] for i in range(0, len(message), 4096)]
    for msg in msgs:
        await event.message.answer(
            msg
        )
        await asyncio.sleep(0.1)




@inject
async def on_change_lang(
        event: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        lang: Lang,
        db: FromDishka[Database],
        cache: FromDishka[Cache],
        tr: FromDishka[Translator]
):
    redis_user, bot_settings = dialog_manager.middleware_data['redis_user'], dialog_manager.middleware_data[
        'bot_settings']
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    redis_user.lang = lang
    await db.user.update(User.id == redis_user.id, values={'lang': lang})
    await cache.user.update_model(redis_user, f'{event.from_user.id}')
    translator = tr.t_hub.get_translator_by_locale(lang.value)
    dialog_manager.middleware_data['translator'] = translator

    await event.message.reply(
        translator.get('ch-lg.ch-kb'),
        reply_markup=menu_frep(
            is_admin=Role.ADMINISTRATOR == redis_user.role,
            translator=translator
        )
    )

    await db.session.commit()


@inject
async def on_change_currency(
        event: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: Currency,
        db: FromDishka[Database],
        cache: FromDishka[Cache]):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    if redis_user.currency != item_id:
        redis_user.currency = item_id
        await db.user.update(
            User.id == redis_user.id,
            {'currency': item_id}
        )
        await cache.user.update_model(redis_user, f'{dialog_manager.event.from_user.id}')
        await db.session.commit()
