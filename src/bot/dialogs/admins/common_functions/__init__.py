from aiogram_dialog import Dialog

from .window import find, user_profile, select_currency, input_amount_change_balance, input_message, mailing, \
    mailing_en, mailing_approve, purchase, refill

common_functions_dialog = Dialog(
    find,
    user_profile,
    select_currency,
    input_amount_change_balance,
    input_message,
    mailing,
    mailing_en,
    mailing_approve,
    purchase,
    refill
)
