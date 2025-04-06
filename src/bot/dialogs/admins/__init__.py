from .products import category_dialog, position_dialog, delete_dialog, item_dialog
from .settings import settings_dialog
from .common_functions import common_functions_dialog
from .payments import payment_dialog
from .statistic import statistic_dialog


admin_dialogs = (
    category_dialog,
    common_functions_dialog,
    position_dialog,
    delete_dialog,
    item_dialog,
    settings_dialog,
    payment_dialog,
    statistic_dialog
)

