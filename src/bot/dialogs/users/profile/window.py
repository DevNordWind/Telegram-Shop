from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Start, Column, Select, StubScroll, LastPage, NextPage, \
    CurrentPage, PrevPage, FirstPage, Row, Button
from aiogram_dialog.widgets.text import Format, Case

from src.bot.states import ProfileState
from src.bot.states.user_states import RefillState
from src.bot.widgets.texts import GetText
from src.db.enums import Lang, Currency
from .callable import on_select_purchase, on_change_lang, on_change_currency, on_unload_items
from .getter import profile_getter, purchases_getter, purchase_details_getter, change_lang_getter, change_currency_btn

profile_window = Window(
    GetText('profile'),

    Group(
        Start(
            GetText('profile.refill-btn'),
            state=RefillState.refill,
            id='refill',
        ),
        SwitchTo(
            GetText('profile.purchases-btn'),
            state=ProfileState.purchases,
            id='purchases'
        ),
        width=2
    ),

    Column(
        SwitchTo(
            GetText('profile.ch-lg-btn'),
            state=ProfileState.ch_lg,
            id='ch_lg'
        ),
        SwitchTo(
            GetText('profile.ch-currency-btn'),
            id='ch_cur',
            state=ProfileState.ch_cur
        ),
    ),

    state=ProfileState.profile,
    getter=profile_getter
)

PURCHASES_SCROLLING = "PURCHASES_SCROLLING"

purchases = Window(

    Case(
        texts={
            True: GetText('purchases'),
            ...: GetText('purchases.none')
        },
        selector=lambda data, widget, manager: bool(data['btns'])
    ),

    Column(
        Select(
            Format('{item[1]}'),
            item_id_getter=lambda x: x[0],
            type_factory=str,
            on_click=on_select_purchase,
            items='btns',
            id='purchase_btn'
        )
    ),

    StubScroll(id=PURCHASES_SCROLLING, pages="pages"),

    Row(
        FirstPage(
            scroll=PURCHASES_SCROLLING, text=Format("⏮️ {target_page1}"),
            when=(F['current_page'] != 0) & (F['current_page'] != 1),
        ),
        PrevPage(
            scroll=PURCHASES_SCROLLING, text=Format("◀️"),
            when=F['current_page'] != 0
        ),
        CurrentPage(
            scroll=PURCHASES_SCROLLING, text=Format("{current_page1}"),
            when=F['pages'] > 1,
        ),
        NextPage(
            scroll=PURCHASES_SCROLLING, text=Format("▶️"),
            when=F['current_page1'] != F['target_page1']
        ),
        LastPage(
            scroll=PURCHASES_SCROLLING, text=Format("{target_page1} ⏭️"),
            when=(F['target_page1'] != F['current_page1']) & (F['target_page'] != F['current_page1']),
        ),
        when=F['pages'] > 0
    ),

    SwitchTo(
        GetText(
            'back',
        ),
        id='bck',
        state=ProfileState.profile
    ),
    getter=purchases_getter,
    state=ProfileState.purchases
)

purchase_details = Window(
    GetText(
        'purchase-details'
    ),

    Button(
        GetText('purchase-details.unload-items-btn'),
        id='unload_items',
        on_click=on_unload_items,
    ),

    SwitchTo(
        GetText('back'),
        state=ProfileState.purchases,
        id='bck'
    ),

    getter=purchase_details_getter,
    state=ProfileState.purchase_details
)

change_lang = Window(
    GetText(
        'lang-select'
    ),

    Select(
        Format('{item[0]}'),
        id='lang_select_items',
        on_click=on_change_lang,
        type_factory=Lang,
        item_id_getter=lambda x: x[1],
        items='btns'
    ),

    SwitchTo(
        GetText('back'),
        id='bck',
        state=ProfileState.profile
    ),

    getter=change_lang_getter,
    state=ProfileState.ch_lg
)

change_currency = Window(
    GetText('ch-cur'),

    Select(
        Case(
            {
                True: Format('✔️ {item.name}'),
                ...: Format('{item.name}'),
            },
            selector=lambda data, widget, manager: data['item'].is_current,
        ),
        on_click=on_change_currency,
        item_id_getter=lambda x: x.id,
        type_factory=Currency,
        id='cur_btn',
        items='btns'
    ),

    SwitchTo(
        GetText('back'),
        state=ProfileState.profile,
        id='back'
    ),
    getter=change_currency_btn,
    state=ProfileState.ch_cur
)
