from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.states import ItemManagementState, PositionManagementState
from src.db import Database


async def on_start_dialog(any: Any, dialog_manager: DialogManager):
    if dialog_manager.start_data != {} and dialog_manager.start_data is not None:
        dialog_manager.dialog_data.update(
            **dialog_manager.start_data
        )
        dialog_manager.start_data.clear()


async def on_select_category_add_item(
        event: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        category_id_fk: int
):
    dialog_manager.dialog_data.update(
        {
            'category_id_fk': category_id_fk
        }
    )
    return await dialog_manager.switch_to(
        ItemManagementState.select_position_add_items
    )


async def on_select_position_add_item(
        event: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        position_id_fk: int
):
    dialog_manager.dialog_data.update(
        {
            'position_id_fk': position_id_fk
        }
    )
    return await dialog_manager.switch_to(
        ItemManagementState.input_items
    )


def clear_list(get_list: list) -> list:
    unwanted = {"", " ", ".", ",", "\r", "\n"}
    return [item for item in get_list if item not in unwanted]


def get_data(dialog_manager: DialogManager) -> tuple[int, int]:
    if dialog_manager.dialog_data == {}:
        return int(dialog_manager.start_data['category_id_fk']), int(dialog_manager.start_data['position_id_fk'])
    return int(dialog_manager.dialog_data.get('category_id_fk')), int(dialog_manager.dialog_data.get('position_id_fk'))


@inject
async def on_input_items(
        event: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        items: str,
        db: FromDishka[Database]
):
    category_id_fk, position_id_fk = get_data(dialog_manager)
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']

    items = clear_list(get_list=items.split("\n\n"))
    for item in items:
        await db.item.new(
            category_id_fk=category_id_fk,
            position_id_fk=position_id_fk,
            content=item
        )
    await db.session.commit()

    await event.reply(
        text=translator.get('input-items.success-input', count_items=len(items))
    )


async def on_complete_download(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
):
    category_id_fk, position_id_fk = get_data(dialog_manager)
    return await dialog_manager.start(
        PositionManagementState.edit_position,
        data={
            'position_id': position_id_fk,
            'category_id_fk': category_id_fk
        },
        mode=StartMode.RESET_STACK
    )
