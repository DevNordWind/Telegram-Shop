from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button
from aiogram_dialog.widgets.text import Case

from src.bot.dialogs.admins.payments.callable import on_cb_switch
from src.bot.dialogs.admins.payments.getter import cryptobot_getter, cryptobot_info_getter
from src.bot.states import PaymentManagementState
from src.bot.widgets import GetText

cryptobot = Window(
    GetText('payment-management'),

    SwitchTo(
        GetText('payment-management.info-btn'),
        id='info',
        state=PaymentManagementState.cryptobot_info
    ),

    Button(
        Case(
            {
                True: GetText('payment-management.status-on-btn'),
                ...: GetText('payment-management.status-off-btn'),
            },
            selector=lambda data, widget, manager: data['status_cryptobot']
        ),
        on_click=on_cb_switch,
        id='on_cryptobot_switch'
    ),

    getter=cryptobot_getter,
    state=PaymentManagementState.cryptobot
)

cryptobot_info = Window(
    Case(
        texts={
            True: GetText('cryptobot-on'),
            ...: GetText('cryptobot-fail-check')
        },
        selector=lambda data, widget, manager: not 'profile' in data
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='back',
        state=PaymentManagementState.cryptobot
    ),
    getter=cryptobot_info_getter,
    state=PaymentManagementState.cryptobot_info
)
