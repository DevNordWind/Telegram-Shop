from aiogram_dialog import Dialog

from .window import profile_window, purchases, purchase_details, change_lang, change_currency

profile_dialog = Dialog(
    profile_window,
    purchases,
    purchase_details,
    change_lang,
    change_currency
)