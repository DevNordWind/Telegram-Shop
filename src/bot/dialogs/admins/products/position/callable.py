from decimal import Decimal, InvalidOperation
from typing import Any

from aiofiles import os
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, File
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, SwitchTo
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.states import PositionManagementState, ItemManagementState
from src.bot.utilities.media_helper import MediaHelper
from src.configuration import conf
from src.db import Database
from src.db.models import Position, Item


async def on_sel_category(event: CallbackQuery, widget: Select, dialog_manager: DialogManager, id: int):
    dialog_manager.dialog_data.update(
        {
            'category_id_fk': id
        }
    )

    await dialog_manager.switch_to(
        PositionManagementState.input_position_name_ru
    )


async def on_select_category_edit_position(event: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                           id: int):
    dialog_manager.dialog_data.update(
        {
            'category_id_fk': id
        }
    )

    await dialog_manager.switch_to(
        PositionManagementState.positions_list
    )


@inject
async def on_add_position_name(event: Message, widget: TextInput, dialog_manager: DialogManager, name: str,
                               db: FromDishka[Database]):
    dialog_manager.dialog_data.update(
        {
            f'{widget.widget_id}_name': name
        }
    )
    await dialog_manager.next()


@inject
async def on_add_position_name_edit(
        event: Message,
        widget: TextInput,
        dialog_manager: DialogManager,
        name: str,
        db: FromDishka[Database]
):
    await db.position.update_names(
        position_id=int(dialog_manager.dialog_data.get('position_id')),
        name_en=name,
        name_ru=dialog_manager.dialog_data.get('ru_name')
    )
    await db.session.commit()
    return await dialog_manager.switch_to(
        PositionManagementState.edit_position
    )


async def on_add_position_price(event: Message, widget: TextInput, dialog_manager: DialogManager, price: Decimal):
    dialog_manager.dialog_data.update(
        {
            f'{widget.widget_id}_price': str(price)
        }
    )
    await dialog_manager.next()


@inject
async def on_add_position_price_edit(event: Message, widget: TextInput, dialog_manager: DialogManager, price: Decimal,
                                     db: FromDishka[Database]):
    price_rub = Decimal(dialog_manager.dialog_data.get('ru_price'))
    price_usd = price
    await db.position.update_prices(int(dialog_manager.dialog_data.get('position_id')), price_rub, price_usd)
    await db.session.commit()
    return await dialog_manager.switch_to(PositionManagementState.edit_position)


async def on_add_position_description(event: Message, widget: TextInput, dialog_manager: DialogManager,
                                      description: str):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    try:
        await (await event.answer(event.text)).delete()
    except TelegramBadRequest:
        return await event.reply(translator.get('errors.html-error-msg'))

    dialog_manager.dialog_data.update(
        {
            f'{widget.widget_id}_description': description
        }
    )
    await dialog_manager.next()


@inject
async def on_add_position_description_edit(
        event: Message,
        widget: TextInput,
        dialog_manager: DialogManager,
        description: str,
        db: FromDishka[Database]
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']

    try:
        await (await event.answer(event.text)).delete()
    except TelegramBadRequest:
        return await event.reply(translator.get('errors.html-error-msg'))

    position_id: int = int(dialog_manager.dialog_data['position_id'])
    await db.position.update_description(
        position_id,
        dialog_manager.dialog_data.get('ru_description'),
        description
    )
    await db.session.commit()
    return await dialog_manager.switch_to(PositionManagementState.edit_position)


@inject
async def on_add_position_media(
        event: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        media_helper: FromDishka[MediaHelper],
        **kwargs
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    helper = media_helper.get_event(event)
    try:
        media: File = await helper.obtain_media(event)
    except TelegramBadRequest as e:
        if e.message == "Telegram server says - Bad Request: file is too big":
            text = translator.get('errors.file-is-to-big-msg')
        else:
            text = translator.get('errors.unexpected-error-msg')
        return await event.reply(
            text=text
        )
    ext = media.file_path.split('.')[-1]
    await helper.bot.send_chat_action(
        event.from_user.id,
        action=f'upload_photo' if helper.content_type == ContentType.PHOTO else 'upload_video'
    )
    dialog_manager.dialog_data.update(
        {
            'file_id': media.file_id,
            'content_type': helper.content_type
        }
    )
    position = await create_position(dialog_manager, db)
    destination = f'{conf.data.position_media_path}/media_{position.id}.{ext}'
    await helper.download_media(
        media.file_id, destination
    )
    position.file_path = destination

    await db.session.commit()

    await dialog_manager.switch_to(
        PositionManagementState.edit_position
    )


@inject
async def on_add_position_media_edit(
        event: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        media_helper: FromDishka[MediaHelper],
        **kwargs
):
    position_id: int = int(dialog_manager.dialog_data.get('position_id'))

    helper = media_helper.get_event(event)
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    try:
        media = await helper.obtain_media(event)
    except TelegramBadRequest as e:
        if e.message == "Bad Request: file is too big":
            text = translator.get('errors.file-is-to-big-msg')
        else:
            text = translator.get('errors.unexpected-error-msg')
        return await event.reply(
            text=text
        )
    await helper.bot.send_chat_action(
        event.from_user.id,
        action=f'upload_photo' if helper.content_type == ContentType.PHOTO else 'upload_video'
    )
    ext = media.file_path.split('.')[-1]
    position = await db.position.get_by_where(
        Position.id == position_id
    )

    destination = f'{conf.data.position_media_path}/media_{position.id}.{ext}'
    if position.file_path:
        await os.remove(
            position.file_path
        )

    await helper.download_media(
        file_id=media.file_id,
        destination=destination
    )

    position.file_path = destination
    position.file_id = media.file_id
    position.content_type = helper.content_type
    await db.session.commit()
    await dialog_manager.switch_to(
        PositionManagementState.edit_position
    )


@inject
async def on_skip_photo(event: CallbackQuery, widget: SwitchTo, dialog_manager: DialogManager,
                        db: FromDishka[Database]):
    await create_position(dialog_manager, db)
    await db.session.commit()


def get_category_id_fk(dialog_data: dict, start_data: dict) -> int:
    if dialog_data.get('category_id_fk') is not None:
        return int(dialog_data.get('category_id_fk'))
    return int(start_data.get('category_id_fk'))


async def create_position(dialog_manager: DialogManager, db: Database) -> Position:
    data = dialog_manager.dialog_data
    position = await db.position.create_position(
        category_id_fk=get_category_id_fk(data, dialog_manager.start_data),
        content_type=dialog_manager.dialog_data.get('content_type'),
        ru_name=data['ru_name'],
        en_name=data['en_name'],
        ru_price=Decimal(data['ru_price']),
        en_price=Decimal(data['en_price']),
        ru_description=data.get('ru_description'),
        en_description=data.get('en_description'),
        file_id=data.get('file_id')
    )
    await db.session.flush()
    data.clear()
    data.update(
        {
            'position_id': position.id
        }
    )
    return position


async def on_select_position(event: CallbackQuery, widget: Button, dialog_manager: DialogManager, item_id: int):
    dialog_manager.dialog_data.update(
        {
            'position_id': item_id
        }
    )
    return await dialog_manager.switch_to(PositionManagementState.edit_position)


async def on_edit_mode(event: CallbackQuery, widget: SwitchTo, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(
        {
            'edit_mode': True
        }
    )


async def on_invalid_number(
        event: Message,
        widget: Any,
        dialog_manager: DialogManager,
        error: InvalidOperation,
):
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    return await event.reply(
        text=translator.get('errors.invalid-number-msg')
    )


@inject
async def on_delete_position(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    position_id = int(dialog_manager.dialog_data.get('position_id'))
    position = await db.position.get_by_where(Position.id == position_id)
    if position.file_path:
        await os.remove(position.file_path)
    await db.session.delete(position)
    await db.session.commit()

    await dialog_manager.switch_to(
        PositionManagementState.positions_list
    )


async def start_items(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
):
    if dialog_manager.dialog_data.get('category_id_fk') is None:
        if dialog_manager.start_data.get('category_id_fk') is not None:
            dialog_manager.dialog_data.update(
                {
                    'category_id_fk': dialog_manager.start_data.get('category_id_fk')
                }
            )
    return await dialog_manager.start(
        ItemManagementState.input_items,
        data={
            'category_id_fk': dialog_manager.dialog_data.get('category_id_fk'),
            'position_id_fk': dialog_manager.dialog_data.get('position_id'),
        },
        mode=StartMode.RESET_STACK
    )


async def on_start(data: Any, dialog_manager: DialogManager, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(
            {
                **dialog_manager.start_data
            }
        )
    if dialog_manager.start_data is not None:
        if 'category_id_fk' in dialog_manager.start_data:
            dialog_manager.dialog_data.update(
                {
                    'category_id_fk': dialog_manager.start_data['category_id_fk']
                }
            )


@inject
async def on_clear_items(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    await db.item.clear(
        dialog_manager.dialog_data['position_id']
    )
    await db.session.commit()
    return await dialog_manager.switch_to(
        PositionManagementState.edit_position
    )


async def on_select_item(
        event: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: int
):
    dialog_manager.dialog_data.update(
        {
            'item_id': item_id
        }
    )
    return await dialog_manager.switch_to(
        PositionManagementState.item_details
    )


@inject
async def on_delete_item(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    item_id = dialog_manager.dialog_data.get('item_id')
    await db.item.delete(Item.id == item_id)
    await db.session.commit()
    await dialog_manager.switch_to(
        PositionManagementState.items_list
    )
