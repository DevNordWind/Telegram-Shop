from aiogram_dialog import Dialog

from .window import refill_window, select_payment_method_window

refill_dialog = Dialog(
    refill_window,
    select_payment_method_window,
)
