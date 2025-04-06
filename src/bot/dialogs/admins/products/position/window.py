from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import MagicData
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Select, Column, Cancel, Group, Button, StubScroll, Row, FirstPage, \
    PrevPage, CurrentPage, NextPage, LastPage
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Case

from src.bot.states import PositionManagementState
from src.bot.widgets import GetText, Refresh, TextInputDecimal
from .callable import (
    on_add_position_name,
    on_add_position_price,
        on_add_position_description,
    on_add_position_media,
    on_sel_category,
    on_skip_photo,
    on_select_position,
    on_select_category_edit_position,
    on_edit_mode,
    on_add_position_name_edit,
    on_add_position_price_edit,
    on_add_position_media_edit,
    on_invalid_number,
    on_add_position_description_edit,
    on_delete_position,
    start_items,
    on_clear_items,
    on_select_item, on_delete_item
)
from .getter import (
    category_list_getter,
    edit_position_getter,
    positions_list_getter,
    add_position_name_ru_getter,
    add_position_price_rub_getter,
    add_position_photo_getter,
    add_position_description_ru_getter, items_list_getter, item_details_getter
)
from ..callable import on_change_lang

CATEGORIES_SCROLL = "CATEGORIES_SCROLL_SELECT"

select_category_add_position = Window(
    GetText('select-category-add-position'),
    Column(
        Select(
            Format('{item[1]}'),
            item_id_getter=lambda x: x[0],
            type_factory=int,
            on_click=on_sel_category,
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
        when=F['btns'] != []
    ),

    getter=category_list_getter,
    state=PositionManagementState.select_category_add_position
)

add_position_name_ru = Window(
    GetText(
        'add-position.ru-name'
    ),

    TextInput(
        on_success=on_add_position_name,
        id='ru'
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.select_category_add_position,
        id='bck',
        when=~F['switch_from_category'] & ~F['edit_mode']
    ),
    SwitchTo(
        GetText(
            'back'
        ),
        id='bck_to_edit',
        when=F['edit_mode'],
        state=PositionManagementState.edit_position
    ),

    Cancel(
        GetText(
            'back'
        ),
        id='bck_category',
        when=F['switch_from_category']
    ),

    getter=add_position_name_ru_getter,
    state=PositionManagementState.input_position_name_ru
)

add_position_name_en = Window(
    GetText(
        'add-position.en-name'
    ),

    TextInput(
        on_success=on_add_position_name,
        id='en',
        filter=MagicData(~F.dialog_manager.dialog_data.get('edit_mode'))
    ),
    TextInput(
        on_success=on_add_position_name_edit,
        id='en',
        filter=MagicData(F.dialog_manager.dialog_data.get('edit_mode') == True)
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.input_position_name_ru,
        id='bck'
    ),

    state=PositionManagementState.input_position_name_en
)

add_position_price_rub = Window(
    GetText(
        'add-position.ru-price'
    ),

    TextInputDecimal(
        on_success=on_add_position_price,
        on_error=on_invalid_number,
        id='ru',
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.input_position_name_en,
        id='bck',
        when=~F['edit_mode']
    ),
    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.edit_position,
        id='bck_edit',
        when=F['edit_mode']
    ),

    getter=add_position_price_rub_getter,
    state=PositionManagementState.input_position_price_rub
)

add_position_price_usd = Window(
    GetText(
        'add-position.en-price'
    ),

    TextInputDecimal(
        on_success=on_add_position_price,
        on_error=on_invalid_number,
        id='en',
        filter=MagicData(~F.dialog_manager.dialog_data.get('edit_mode'))
    ),

    TextInputDecimal(
        on_success=on_add_position_price_edit,
        on_error=on_invalid_number,
        id='en',
        filter=MagicData(F.dialog_manager.dialog_data.get('edit_mode') == True)
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.input_position_price_rub,
        id='bck'
    ),
    state=PositionManagementState.input_position_price_usd
)

add_position_description_ru = Window(
    GetText(
        'add-position.ru-description'
    ),

    TextInput(
        on_success=on_add_position_description,
        id='ru',
        type_factory=str
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.edit_position,
        id='back_to_edit',
        when=F['edit_mode']
    ),

    Column(
        SwitchTo(
            GetText(
                'skip'
            ),
            state=PositionManagementState.input_position_photo,
            id='skip'
        ),

        SwitchTo(
            GetText(
                'back'
            ),
            state=PositionManagementState.input_position_price_usd,
            id='bck'
        ),
        when=~F['edit_mode']
    ),

    getter=add_position_description_ru_getter,
    state=PositionManagementState.input_position_description_ru
)

add_position_description_en = Window(
    GetText(
        'add-position.en-description'
    ),

    TextInput(
        on_success=on_add_position_description,
        id='en',
        type_factory=str,
        filter=MagicData(~F.dialog_manager.dialog_data.get('edit_mode'))
    ),

    TextInput(
        on_success=on_add_position_description_edit,
        id='en_edit',
        type_factory=str,
        filter=MagicData(F.dialog_manager.dialog_data.get('edit_mode') == True)
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.input_position_description_ru,
        id='bck'
    ),
    state=PositionManagementState.input_position_description_en
)

add_position_media = Window(
    GetText(
        'add-position.media'
    ),

    MessageInput(
        content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION],
        func=on_add_position_media,
        filter=~MagicData(F.dialog_manager.dialog_data.get('edit_mode'))
    ),

    MessageInput(
        content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION],
        func=on_add_position_media_edit,
        filter=MagicData(F.dialog_manager.dialog_data.get('edit_mode') == True)
    ),

    SwitchTo(
        id='skip_photo',
        on_click=on_skip_photo,
        state=PositionManagementState.edit_position,
        text=GetText('skip'),
        when=~F['edit_mode']
    ),

    SwitchTo(
        GetText('back'),
        state=PositionManagementState.edit_position,
        id='back_to_edit',
        when=F['edit_mode']
    ),

    getter=add_position_photo_getter,
    state=PositionManagementState.input_position_photo
)

edit_position = Window(
    GetText(
        'edit-position'
    ),

    DynamicMedia(
        'media',
        when=F['is_media'] == 'True'
    ),

    Group(
        SwitchTo(
            GetText(
                'edit-position.edit-name-btn'
            ),
            on_click=on_edit_mode,
            state=PositionManagementState.input_position_name_ru,
            id='edit_btn_name'
        ),

        SwitchTo(
            GetText(
                'edit-position.edit-price-btn'
            ),
            on_click=on_edit_mode,
            state=PositionManagementState.input_position_price_rub,
            id='edit_btn_price'
        ),

        SwitchTo(
            GetText(
                'edit-position.edit-media-btn'
            ),
            on_click=on_edit_mode,
            state=PositionManagementState.input_position_photo,
            id='edit_photo_btn'
        ),

        SwitchTo(
            GetText(
                'edit-position.edit-description-btn'
            ),
            on_click=on_edit_mode,
            state=PositionManagementState.input_position_description_ru,
            id='edit_description_btn'
        ),

        Button(
            GetText(
                'edit-position.add-items-btn'
            ),
            on_click=start_items,
            id='add_items_btn',
        ),

        SwitchTo(
            GetText(
                'edit-position.clear-items-btn'
            ),
            state=PositionManagementState.clear_items,
            id='edit_btn'
        ),

        SwitchTo(
            GetText(
                'edit-position.delete-item-btn'
            ),
            id='delete_item',
            state=PositionManagementState.items_list
        ),

        Button(
            GetText(
                'edit-position.copy-link-btn'
            ),
            id='edit_btn'
        ),

        SwitchTo(
            GetText(
                'edit-position.delete-btn'
            ),
            state=PositionManagementState.delete,
            id='delete_btn'
        ),

        width=2,
    ),

    Button(
        Case(
            texts={
                True: GetText('edit-position.back-another-lang-btn'),
                ...: GetText('edit-position.another-lang-btn')
            },
            selector=lambda data, widget, manager: bool(manager.dialog_data.get('temp_lang'))
        ),
        on_click=on_change_lang,
        id='on_ch_lg'
    ),

    Refresh(
        GetText('refresh'),
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.positions_list,
        id='back',
        when=F['category_id_fk']
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.select_category_edit_position,
        id='bck_sel_cat',
        when=~F['category_id_fk']
    ),

    getter=edit_position_getter,
    state=PositionManagementState.edit_position
)

positions_list = Window(
    GetText(
        'positions-list'
    ),

    Column(
        Select(
            Format('{item[1]}'),
            item_id_getter=lambda x: x[0],
            type_factory=int,
            on_click=on_select_position,
            items='btns',
            id='position_btns'
        ),
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=PositionManagementState.select_category_edit_position
    ),

    getter=positions_list_getter,
    state=PositionManagementState.positions_list
)

select_category_edit_position = Window(
    GetText('select-category-edit-position'),

    Column(
        Select(
            text=Format('{item[1]}'),
            items='btns',
            item_id_getter=lambda x: x[0],
            type_factory=int,
            on_click=on_select_category_edit_position,
            id='cat_btns'
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
        when=(F['btns'] != []) & (F['pages'] > 0)
    ),

    getter=category_list_getter,
    state=PositionManagementState.select_category_edit_position
)

delete_position = Window(
    GetText(
        'delete-position'
    ),

    Button(
        GetText('delete-position.approve-btn'),
        on_click=on_delete_position,
        id='delete_position',
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.edit_position,
        id='bck'
    ),

    state=PositionManagementState.delete
)

clear_items = Window(
    GetText(
        'clear-items'
    ),

    Button(
        GetText('clear-items.approve-btn'),
        on_click=on_clear_items,
        id='clear_items',
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.edit_position,
        id='bck'
    ),
    state=PositionManagementState.clear_items
)

ITEMS_SCROLL = "ITEMS_SCROLL"

items_list = Window(

    Case(
        {
            True: GetText('items-list'),
            ...: GetText('items-list.items-list-empty')
        },
        selector=lambda data, widget, manager: data['btns'] != []
    ),
    Column(
        Select(
            Format('{item[1]}'),
            item_id_getter=lambda x: x[0],
            items='btns',
            type_factory=int,
            id='item_btn',
            on_click=on_select_item,
        ),
    ),

    StubScroll(id=ITEMS_SCROLL, pages="pages"),

    Row(
        FirstPage(
            scroll=ITEMS_SCROLL, text=Format("⏮️ {target_page1}"),
            when=(F['current_page'] != 0) & (F['current_page'] != 1),
        ),
        PrevPage(
            scroll=ITEMS_SCROLL, text=Format("◀️"),
            when=F['current_page'] != 0
        ),
        CurrentPage(
            scroll=ITEMS_SCROLL, text=Format("{current_page1}"),
        ),
        NextPage(
            scroll=ITEMS_SCROLL, text=Format("▶️"),
            when=F['current_page1'] != F['target_page1']
        ),
        LastPage(
            scroll=ITEMS_SCROLL, text=Format("{target_page1} ⏭️"),
            when=(F['target_page1'] != F['current_page1']) & (F['target_page'] != F['current_page1']),
        ),
        when=F['pages'] > 0
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=PositionManagementState.edit_position,
        id='bck'
    ),

    getter=items_list_getter,
    state=PositionManagementState.items_list
)

item_details = Window(
    GetText(
        'items-list.details'
    ),

    SwitchTo(
        GetText(
            'items-list.delete-btn'
        ),
        state=PositionManagementState.delete_item,
        id='delete_item'
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=PositionManagementState.items_list
    ),

    getter=item_details_getter,
    state=PositionManagementState.item_details
)

delete_item = Window(
    GetText(
        'delete-item'
    ),

    Button(
        GetText(
            'delete-item.approve-btn'
        ),
        on_click=on_delete_item,
        id='del_item'
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=PositionManagementState.item_details
    ),

    getter=item_details_getter,
    state=PositionManagementState.delete_item
)
