from aiogram_dialog import Dialog

from .callable import on_start_dialog

from .window import select_category_add_items, select_position_add_items, input_items

item_dialog = Dialog(
    select_category_add_items,
    select_position_add_items,
    input_items,
    on_start=on_start_dialog,
)
