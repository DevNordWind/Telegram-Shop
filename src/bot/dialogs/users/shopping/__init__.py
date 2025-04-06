from aiogram_dialog import Dialog

from .window import (
    select_category,
    select_position,
    position_deteails,
    not_enough_money,
    input_amount_item,
    approve_buy,
    receipt
)

shopping_dialog = Dialog(
    select_category,
    select_position,
    position_deteails,
    not_enough_money,
    input_amount_item,
    approve_buy,
    receipt
)