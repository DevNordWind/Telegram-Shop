from aiogram import F
from aiogram.filters import MagicData
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Cancel
from aiogram_dialog.widgets.text import Case

from src.bot.states.user_states import RefillState
from src.bot.widgets import TextInputDecimal
from src.bot.widgets.texts import GetText
from .callable import on_refill_input_success, on_refill_input_error, on_select_payment_method
from .getter import select_payment_method_getter, refill_getter

refill_window = Window(
    Case(
        {
            True: GetText('refill'),
            ...: GetText('refill-disable')
        },
        selector=lambda data, widget, manager: data['is_refill_enable']
    ),

    TextInputDecimal(
        on_success=on_refill_input_success,
        on_error=on_refill_input_error,
        id='id',
        filter=MagicData(F.dialog_manager.dialog_data.get('is_refill_enable'))
    ),

    Cancel(
        GetText(
            'back'
        ),
    ),
    getter=refill_getter,
    state=RefillState.refill
)

select_payment_method_window = Window(
    GetText(
        'select-payment-method'
    ),

    Button(
        GetText('select-payment-method.cryptobot-btn'),
        id='CRYPTOBOT',
        on_click=on_select_payment_method,
        when=F['status_cryptobot']
    ),

    SwitchTo(
        GetText('back'),
        state=RefillState.refill,
        id='bck'
    ),
    getter=select_payment_method_getter,
    state=RefillState.select_payment_method
)
