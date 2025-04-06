from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from src.bot.states import DeleteProductsState
from src.bot.widgets import GetText

from .callable import (
    on_delete_positions,
    on_delete_categories,
    on_delete_items
)
from .getter import (
    approve_delete_categories_getter,
    approve_delete_positions_getter,
    approve_delete_items_getter,
)

delete = Window(
    GetText(
        'delete'
    ),

    SwitchTo(
        GetText(
            'delete.delete-categories-btn'
        ),
        state=DeleteProductsState.approve_delete_categories,
        id='approve_categories'
    ),

    SwitchTo(
        GetText(
            'delete.delete-positions-btn'
        ),
        state=DeleteProductsState.approve_delete_positions,
        id='approve_positions'
    ),

    SwitchTo(
        GetText(
            'delete.delete-items-btn'
        ),
        state=DeleteProductsState.approve_delete_items,
        id='items'
    ),

    state=DeleteProductsState.delete
)

approve_delete_categories = Window(

    GetText(
        'approve-delete-categories'
    ),

    Button(
        GetText(
            'approve-delete-categories.approve-btn'
        ),
        id='approve',
        on_click=on_delete_categories
    ),

    SwitchTo(
        GetText('back'),
        id='bck',
        state=DeleteProductsState.delete
    ),

    getter=approve_delete_categories_getter,
    state=DeleteProductsState.approve_delete_categories
)

approve_delete_positions = Window(

    GetText(
        'approve-delete-positions'
    ),

    Button(
        GetText(
            'approve-delete-positions.approve-btn'
        ),
        id='approve',
        on_click=on_delete_positions
    ),

    SwitchTo(
        GetText('back'),
        id='bck',
        state=DeleteProductsState.delete
    ),

    getter=approve_delete_positions_getter,
    state=DeleteProductsState.approve_delete_positions
)

approve_delete_items = Window(

    GetText(
        'approve-delete-items'
    ),

    Button(
        GetText(
            'approve-delete-items.approve-btn'
        ),
        id='approve',
        on_click=on_delete_items
    ),

    SwitchTo(
        GetText('back'),
        id='bck',
        state=DeleteProductsState.delete
    ),

    getter=approve_delete_items_getter,
    state=DeleteProductsState.approve_delete_items
)
