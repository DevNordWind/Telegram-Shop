from aiogram import F
from aiogram.filters import MagicData
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group, CopyText, Column, Select, StubScroll, LastPage, \
    NextPage, CurrentPage, PrevPage, FirstPage, Row
from aiogram_dialog.widgets.text import Format, Case

from src.bot.states import CategoryManagementState
from src.bot.widgets import GetText, Refresh
from .callable import (
    on_add_category_success,
    on_delete_category,
    on_select_category,
    on_add_position,
    on_edit_name,
    on_add_category_en_success_edit,
    on_add_category_en_success,
)
from .getter import (
    edit_category_getter,
    category_list_getter,
    input_category_name_ru_getter,
)
from ..callable import on_change_lang

input_category_name_ru = Window(
    GetText(
        'input-category-name'
    ),

    TextInput(
        on_success=on_add_category_success,
        id='on_success'
    ),

    SwitchTo(
        GetText('back'),
        state=CategoryManagementState.edit_category,
        when=F['edit_mode'],
        id='back'
    ),
    getter=input_category_name_ru_getter,
    state=CategoryManagementState.input_category_name_ru
)

input_category_name_en = Window(
    GetText(
        'input-category-name.en'
    ),

    TextInput(
        on_success=on_add_category_en_success,
        id='on_en_success',
        filter=MagicData(~F.dialog_manager.dialog_data['edit_mode'])
    ),

    TextInput(
        on_success=on_add_category_en_success_edit,
        id='on_en_success_edit',
        filter=MagicData(F.dialog_manager.dialog_data['edit_mode'] == True)
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=CategoryManagementState.input_category_name_ru
    ),
    state=CategoryManagementState.input_category_name_en
)

edit_category = Window(
    GetText(
        'edit-category'
    ),
    Group(
        SwitchTo(
            GetText(
                'edit-category.edit-name-btn'
            ),
            on_click=on_edit_name,
            state=CategoryManagementState.input_category_name_ru,
            id='edit_name'
        ),
        Button(
            GetText(
                'edit-category.add-position-btn'
            ),
            on_click=on_add_position,
            id='add_position'
        ),
        CopyText(
            GetText(
                'edit-category.copy-link-btn'
            ),
            copy_text=Format('{copy_link}'),
        ),
        SwitchTo(
            GetText(
                'edit-category.delete-btn'
            ),
            state=CategoryManagementState.delete_category,
            id='delete'
        ),
        width=2
    ),

    Button(
        Case(
            texts={
                True: GetText('edit-category.back-another-lang-btn'),
                ...: GetText('edit-category.another-lang-btn')
            },
            selector=lambda data, widget, manager: bool(manager.dialog_data.get('temp_lang'))
        ),
        on_click=on_change_lang,
        id='on_ch_lg'
    ),

    Refresh(
        GetText('refresh')
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=CategoryManagementState.categories_list,
        id='back_to_category'
    ),
    getter=edit_category_getter,
    state=CategoryManagementState.edit_category
)

delete_category = Window(
    GetText(
        'delete-category'
    ),

    Button(
        GetText(
            'delete-category.approve-btn'
        ),
        id='btn',
        on_click=on_delete_category
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=CategoryManagementState.edit_category,
        id='bck'
    ),
    state=CategoryManagementState.delete_category
)

CATEGORIES_SCROLL = "CATEGORIES_SCROLL"

categories_list = Window(

    GetText(
        'categories-list'
    ),

    Column(
        Select(
            Format('{item[1]}'),
            item_id_getter=lambda x: x[0],
            type_factory=int,
            on_click=on_select_category,
            items='btns',
            id='category_btns'
        ),
    ),

    StubScroll(id=CATEGORIES_SCROLL, pages="pages"),

    Row(
        FirstPage(
            scroll=CATEGORIES_SCROLL, text=Format("⏮️ {target_page1}"),
            when=(F['current_page'] != 0) & (F['current_page'] != 1),
        ),
        PrevPage(
            scroll=CATEGORIES_SCROLL, text=Format("◀️"),
            when=F['current_page'] != 0
        ),
        CurrentPage(
            scroll=CATEGORIES_SCROLL, text=Format("{current_page1}"),
        ),
        NextPage(
            scroll=CATEGORIES_SCROLL, text=Format("▶️"),
            when=F['current_page1'] != F['target_page1']
        ),
        LastPage(
            scroll=CATEGORIES_SCROLL, text=Format("{target_page1} ⏭️"),
            when=(F['target_page1'] != F['current_page1']) & (F['target_page'] != F['current_page1']),
        ),
        when=F['pages'] > 0
    ),

    getter=category_list_getter,
    state=CategoryManagementState.categories_list
)
