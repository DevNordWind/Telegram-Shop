from aiogram import F
from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import StubScroll, Row, FirstPage, PrevPage, CurrentPage, NextPage, LastPage, Column, \
    Select, SwitchTo, Button, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Case

from src.bot.states import ShoppingState, RefillState
from src.bot.widgets import GetText
from .callable import on_select_category, on_select_position, on_buy, on_item_input_error, on_item_input_success, \
    on_approve_buy
from .getter import select_position_getter, select_category_getter, position_details_getter, input_amount_item_getter, \
    approve_buy_getter, receipt_getter

CATEGORIES_SCROLL = "CATEGORIES_SCROLL"

select_category = Window(
    Case(
        texts={
            True: GetText('select-category'),
            ...: GetText('select-category.unavailable')
        },
        selector=lambda data, widget, manager: bool(data['status_buy']) and bool('btns')
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
        when=F['status_buy']
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
            when=F['pages'] > 1
        ),
        NextPage(
            scroll=CATEGORIES_SCROLL, text=Format("▶️"),
            when=F['current_page1'] != F['target_page1']
        ),
        LastPage(
            scroll=CATEGORIES_SCROLL, text=Format("{target_page1} ⏭️"),
            when=(F['target_page1'] != F['current_page1']) & (F['target_page'] != F['current_page1']),
        ),
        when=(F['pages'] > 0) & (F['status_buy'])
    ),

    getter=select_category_getter,
    state=ShoppingState.select_category
)

POSITION_SCROLL = "POSITION_SCROLL"

select_position = Window(
    GetText('select-position'),

    Column(
        Select(
            Format('{item[1]} | {item[2]}{item[3]}'),
            item_id_getter=lambda x: x[0],
            type_factory=int,
            on_click=on_select_position,
            items='btns',
            id='position_btns'
        ),
    ),

    StubScroll(id=POSITION_SCROLL, pages="pages"),

    Row(
        FirstPage(
            scroll=POSITION_SCROLL, text=Format("⏮️ {target_page1}"),
            when=(F['current_page'] != 0) & (F['current_page'] != 1),
        ),
        PrevPage(
            scroll=POSITION_SCROLL, text=Format("◀️"),
            when=F['current_page'] != 0
        ),
        CurrentPage(
            scroll=POSITION_SCROLL, text=Format("{current_page1}"),
            when=F['pages'] > 1,
        ),
        NextPage(
            scroll=POSITION_SCROLL, text=Format("▶️"),
            when=F['current_page1'] != F['target_page1']
        ),
        LastPage(
            scroll=POSITION_SCROLL, text=Format("{target_page1} ⏭️"),
            when=(F['target_page1'] != F['current_page1']) & (F['target_page'] != F['current_page1']),
        ),
        when=F['pages'] > 0
    ),

    SwitchTo(
        GetText('back'),
        id='bck',
        state=ShoppingState.select_category
    ),
    getter=select_position_getter,
    state=ShoppingState.select_position
)

position_deteails = Window(
    Format('{text}'),

    DynamicMedia(
        'media',
        when=F['media'].is_not(None)
    ),

    Button(
        GetText('position-details.buy-btn'),
        id='buy_btn',
        on_click=on_buy,
    ),

    SwitchTo(
        GetText('back'),
        id='back',
        state=ShoppingState.select_position
    ),
    getter=position_details_getter,
    state=ShoppingState.position_details
)

not_enough_money = Window(
    GetText(
        'not-enough-money'
    ),

    Start(
        GetText('not-enough-money.refill-btn'),
        id='refill',
        state=RefillState.refill,
        mode=StartMode.NORMAL
    ),

    SwitchTo(
        GetText('back'),
        state=ShoppingState.position_details,
        id='back'
    ),

    state=ShoppingState.not_enough_money
)

input_amount_item = Window(
    GetText(
        'input-amount-item'
    ),

    TextInput(
        on_success=on_item_input_success,
        on_error=on_item_input_error,
        type_factory=int,
        id='input_items'
    ),

    SwitchTo(
        GetText('back'),
        state=ShoppingState.position_details,
        id='back',
    ),
    getter=input_amount_item_getter,
    state=ShoppingState.input_amount_item
)

approve_buy = Window(
    GetText(
        'approve-buy'
    ),

    Button(
        GetText('approve-buy.buy-btn'),
        id='buy_btn',
        on_click=on_approve_buy,
    ),

    SwitchTo(
        GetText('back'),
        state=ShoppingState.position_details,
        id='to_pos_det',
    ),

    getter=approve_buy_getter,
    state=ShoppingState.approve_buy
)

receipt = Window(
    GetText('receipt'),

    SwitchTo(
        GetText("back"),
        id='bck',
        state=ShoppingState.select_category
    ),
    getter=receipt_getter,
    state=ShoppingState.receipt
)
