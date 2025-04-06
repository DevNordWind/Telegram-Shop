from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Select, Button, Cancel
from aiogram_dialog.widgets.text import Format

from src.bot.states import CommonFunctionsState
from src.bot.widgets import GetText, Refresh, TextInputDecimal
from src.db.enums import Currency
from .callable import on_input_find, on_input_amount_success, on_balance_actions, on_select_currency, on_input_message, \
    on_mailing, on_mailing_en, on_approve, on_unload_items
from .getter import user_profile_getter, select_currency_getter, mailing_approve_getter, refill_getter, purchase_getter

find = Window(
    GetText(
        'find'
    ),
    TextInput(
        on_success=on_input_find,
        id='on_inp_find'
    ),

    state=CommonFunctionsState.find
)

refill = Window(
    GetText('refill-find'),

    getter=refill_getter,
    state=CommonFunctionsState.refill
)

purchase = Window(
    GetText('purchase-find'),

    Button(
        GetText('purchase-find.unload-items-btn'),
        id='unload',
        on_click=on_unload_items
    ),

    getter=purchase_getter,
    state=CommonFunctionsState.purchase
)

user_profile = Window(
    GetText(
        'user-profile'
    ),

    Group(
        SwitchTo(
            text=GetText('user-profile.change-balance-btn'),
            state=CommonFunctionsState.select_currency,
            on_click=on_balance_actions,
            id='withdraw'
        ),
        SwitchTo(
            text=GetText('user-profile.give-balance-btn'),
            state=CommonFunctionsState.select_currency,
            on_click=on_balance_actions,
            id='refill'
        ),

        width=2,
    ),

    Group(
        SwitchTo(
            text=GetText('user-profile.send-msg-btn'),
            state=CommonFunctionsState.input_message,
            id='input_msg'
        ),
        width=2
    ),

    Refresh(
        GetText('refresh'),
        id='refresh'
    ),

    getter=user_profile_getter,
    state=CommonFunctionsState.user_profile
)

select_currency = Window(
    GetText(
        'select-currency'
    ),

    Group(
        Select(
            Format('{item}'),
            item_id_getter=lambda item: item,
            type_factory=Currency,
            items='btns',
            on_click=on_select_currency,
            id='currency_btn'
        ),
        width=2,
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=CommonFunctionsState.user_profile
    ),
    getter=select_currency_getter,
    state=CommonFunctionsState.select_currency
)

input_amount_change_balance = Window(
    GetText(
        'input-amount-change-balance'
    ),

    TextInputDecimal(
        on_success=on_input_amount_success,
        id='on_input_amount'
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=CommonFunctionsState.select_currency
    ),

    state=CommonFunctionsState.input_amount_change_balance
)

input_message = Window(
    GetText(
        'input-message'
    ),

    TextInput(
        id='input_msg',
        on_success=on_input_message
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='bck',
        state=CommonFunctionsState.user_profile
    ),

    state=CommonFunctionsState.input_message
)

mailing = Window(
    GetText(
        'mailing'
    ),
    MessageInput(
        content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION, ContentType.TEXT],
        func=on_mailing,
    ),

    state=CommonFunctionsState.mailing
)

mailing_en = Window(
    GetText('mailing.en'),

    TextInput(
        on_success=on_mailing_en,
        id='mailing_en'
    ),

    SwitchTo(
        GetText('skip'),
        state=CommonFunctionsState.mailing_approve,
        id='to_approve'
    ),

    SwitchTo(
        GetText('back'),
        id='back',
        state=CommonFunctionsState.mailing
    ),

    state=CommonFunctionsState.mailing_en
)

mailing_approve = Window(
    GetText('mailing-approve'),

    Button(
        GetText('mailing-approve.approve-btn'),
        id='approve',
        on_click=on_approve
    ),

    Cancel(
        GetText('mailing-approve.cancel-btn')
    ),
    getter=mailing_approve_getter,
    state=CommonFunctionsState.mailing_approve
)
