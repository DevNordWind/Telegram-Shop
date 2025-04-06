from aiofiles import os
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.bot.states import DeleteProductsState
from src.db import Database
from src.db.models import Item, Position


@inject
async def on_delete_categories(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']

    positions = await db.position.get_many(limit=9999, order_by=Position.id)
    for position in positions:
        if position.file_path:
            await os.remove(
                position.file_path
            )
    await db.category.delete()
    await db.item.delete(
        Item.purchase_id_fk == None
    )
    await db.session.commit()
    await event.message.reply(
        text=translator.get(
            'approve-delete-categories.success-delete',
            **dialog_manager.dialog_data
        )
    )
    await dialog_manager.switch_to(
        DeleteProductsState.delete
    )


@inject
async def on_delete_positions(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    positions = await db.position.get_many(limit=9999, order_by=Position.id)
    for position in positions:
        if position.file_path:
            await os.remove(
                position.file_path
            )
        await db.session.delete(position)
    await db.item.delete(
        Item.purchase_id_fk == None
    )
    await db.session.commit()
    await event.message.reply(
        text=translator.get(
            'approve-delete-positions.success-delete',
            **dialog_manager.dialog_data
        )
    )
    await dialog_manager.switch_to(
        DeleteProductsState.delete
    )


@inject
async def on_delete_items(
        event: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager,
        db: FromDishka[Database]
):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']

    await db.item.delete(
        Item.purchase_id_fk == None
    )
    await db.session.commit()
    await event.message.reply(
        text=translator.get(
            'approve-delete-items.success-delete',
            **dialog_manager.dialog_data
        )
    )
    await dialog_manager.switch_to(
        DeleteProductsState.delete
    )
