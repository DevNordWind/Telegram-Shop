from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Url, Button
from aiogram_dialog.widgets.text import Format

from src.bot.states.user_states import InvoiceState
from src.bot.widgets import GetText
from .callable import on_success, on_error, on_close, on_check_invoice
from .getter import invoice_getter

invoice_window = Window(
    GetText('invoice'),

    Url(
        text=GetText('invoice.pay-btn'),
        url=Format('{pay_url}'),
    ),

    Button(
        GetText('invoice.check-btn'),
        on_click=on_check_invoice,
        id='chck',
    ),

    Button(
        GetText('close'),
        on_click=on_close,
        id='close'
    ),

    TextInput(
        id='handle_close_attempt',
        on_success=on_success,
        on_error=on_error,
    ),

    getter=invoice_getter,
    state=InvoiceState.invoice
)
