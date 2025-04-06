from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button, LastPage, NextPage, CurrentPage, PrevPage, FirstPage, \
    Row, StubScroll, Column, SwitchTo
from aiogram_dialog.widgets.text import Format

from src.bot.states import ItemManagementState
from src.bot.widgets import GetText
from .callable import (
    on_select_category_add_item,
    on_select_position_add_item,
    on_input_items,
    on_complete_download
)
from .getter import (
    select_category_add_item_getter, select_position_add_item_getter
)

CATEGORY_SCROLL = "CATEGORY_SCROLL"

select_category_add_items = Window(
    GetText(
        'select-category-add-items'
    ),

    Column(
        Select(
            Format('{item[1]}'),
            item_id_getter=lambda x: x[0],
            on_click=on_select_category_add_item,
            type_factory=int,
            items='btns',
            id='sel_category'
        ),
    ),

    StubScroll(id=CATEGORY_SCROLL, pages="pages"),

    Row(
        FirstPage(
            scroll=CATEGORY_SCROLL, text=Format("⏮️ {target_page1}"),
            when=(F['current_page'] != 0) & (F['current_page'] != 1),
        ),
        PrevPage(
            scroll=CATEGORY_SCROLL, text=Format("◀️"),
            when=F['current_page'] != 0
        ),
        CurrentPage(
            scroll=CATEGORY_SCROLL, text=Format("{current_page1}"),
        ),
        NextPage(
            scroll=CATEGORY_SCROLL, text=Format("▶️"),
            when=F['current_page1'] != F['target_page1']
        ),
        LastPage(
            scroll=CATEGORY_SCROLL, text=Format("{target_page1} ⏭️"),
            when=(F['target_page1'] != F['current_page1']) & (F['target_page'] != F['current_page1']),
        ),
        when=F['pages'] > 0
    ),

    getter=select_category_add_item_getter,
    state=ItemManagementState.select_category_add_items
)

select_position_add_items = Window(
    GetText(
        'select-position-add-items'
    ),

    Column(
        Select(
            Format(
                '{item[1]}'
            ),
            item_id_getter=lambda x: x[0],
            type_factory=int,
            on_click=on_select_position_add_item,
            items='btns',
            id='position_btns'
        ),
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=ItemManagementState.select_category_add_items
    ),

    getter=select_position_add_item_getter,
    state=ItemManagementState.select_position_add_items
)

input_items = Window(
    GetText(
        'input-items'
    ),

    TextInput(
        on_success=on_input_items,
        type_factory=str,
        id='on_input_items'
    ),

    Button(
        GetText(
            'input-items.complete-download-btn'
        ),
        id='complete_download',
        on_click=on_complete_download
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='back',
        state=ItemManagementState.select_position_add_items
    ),

    state=ItemManagementState.input_items
)
