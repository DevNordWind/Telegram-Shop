from aiogram_dialog import Dialog

from .window import (
    input_category_name_ru,
    input_category_name_en,
    edit_category,
    categories_list,
    delete_category
)

category_dialog = Dialog(
    input_category_name_ru,
    input_category_name_en,
    edit_category,
    categories_list,
    delete_category
)