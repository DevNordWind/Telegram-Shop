from aiogram_dialog import Dialog

from .window import (
    select_category_add_position,
    add_position_name_ru,
    add_position_name_en,
    add_position_price_rub,
    add_position_price_usd,
    add_position_description_ru,
    add_position_description_en,
    add_position_media,
    edit_position,
    positions_list,
    select_category_edit_position,
    delete_position,
    clear_items,
    items_list,
    item_details,
    delete_item
)

from .callable import on_start

position_dialog = Dialog(
    select_category_add_position,
    add_position_name_ru,
    add_position_name_en,
    add_position_price_rub,
    add_position_price_usd,
    add_position_description_ru,
    add_position_description_en,
    add_position_media,
    edit_position,
    positions_list,
    select_category_edit_position,
    delete_position,
    clear_items,
    items_list,
    item_details,
    delete_item,
    on_start=on_start
)
