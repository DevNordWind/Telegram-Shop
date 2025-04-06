from aiogram_dialog import Dialog

from .window import (
    delete,
    approve_delete_categories,
    approve_delete_positions,
    approve_delete_items
)

delete_dialog = Dialog(
    delete,
    approve_delete_categories,
    approve_delete_positions,
    approve_delete_items
)
