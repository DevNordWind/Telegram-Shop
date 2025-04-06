from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.bot.states import PositionManagementState, CategoryManagementState
from src.db import Database
from src.db.enums import Lang
from src.db.models import Category


async def on_add_category_success(event: Message, widget: Any, dialog_manager: DialogManager, category_name: str):
    dialog_manager.dialog_data.update(
        {
            'category_ru_name': category_name
        }
    )
    return await dialog_manager.switch_to(
        state=CategoryManagementState.input_category_name_en
    )


@inject
async def on_add_category_en_success(
        event: Message,
        widget: Any,
        dialog_manager: DialogManager,
        category_name: str,
        db: FromDishka[Database]
):
    dialog_manager.dialog_data.update(
        {
            'category_en_name': category_name
        }
    )
    category = await db.category.create_category(
        category_ru_name=dialog_manager.dialog_data['category_ru_name'],
        category_en_name=dialog_manager.dialog_data['category_en_name']
    )
    await db.session.flush()
    dialog_manager.dialog_data.update(
        {
            'category_id': category.id
        }
    )
    await db.session.commit()
    await dialog_manager.switch_to(
        state=CategoryManagementState.edit_category
    )


@inject
async def on_add_category_en_success_edit(
        event: Message,
        widget: Any,
        dialog_manager: DialogManager,
        category_name: str,
        db: FromDishka[Database]
):
    category_id: int = dialog_manager.dialog_data['category_id']
    category = await db.category.get_with_locales(category_id)
    print(category.category_localized)
    for category_locale in category.category_localized:
        if category_locale.lang == Lang.RU:
            category_locale.name = dialog_manager.dialog_data['category_ru_name']
        elif category_locale.lang == Lang.EN:
            category_locale.name = category_name
    await db.session.commit()
    await dialog_manager.switch_to(
        CategoryManagementState.edit_category
    )


@inject
async def on_delete_category(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    category_id: int = int(dialog_manager.dialog_data['category_id'])
    await db.category.delete(Category.id == category_id)
    await db.session.commit()
    return await dialog_manager.switch_to(
        CategoryManagementState.categories_list
    )


async def on_select_category(event: CallbackQuery, widget: Button, dialog_manager: DialogManager, item_id: int):
    dialog_manager.dialog_data.update(
        {
            'category_id': item_id
        }
    )
    return await dialog_manager.switch_to(CategoryManagementState.edit_category)


async def on_add_position(event: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    return await dialog_manager.start(
        state=PositionManagementState.input_position_name_ru,
        data={
            'category_id_fk': dialog_manager.dialog_data['category_id'],
            'switch_from_category': True
        }
    )


async def on_edit_name(event: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(
        {
            'edit_mode': True
        }
    )
