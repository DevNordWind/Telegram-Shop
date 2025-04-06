from aiogram.fsm.state import StatesGroup, State


class CategoryManagementState(StatesGroup):
    input_category_name_ru = State()
    input_category_name_en = State()
    delete_category = State()
    edit_category = State()
    categories_list = State()


class DeleteProductsState(StatesGroup):
    delete = State()
    approve_delete_categories = State()
    approve_delete_positions = State()
    approve_delete_items = State()


class PositionManagementState(StatesGroup):
    select_category_add_position = State()
    input_position_name_ru = State()
    input_position_name_en = State()
    input_position_price_rub = State()
    input_position_price_usd = State()
    input_position_description_ru = State()
    input_position_description_en = State()
    input_position_photo = State()
    edit_position = State()
    positions_list = State()
    select_category_edit_position = State()
    delete = State()
    clear_items = State()
    upload_items = State()
    items_list = State()
    item_details = State()
    delete_item = State()


class ItemManagementState(StatesGroup):
    select_category_add_items = State()
    select_position_add_items = State()
    input_items = State()


class SettingsState(StatesGroup):
    change_data = State()
    start_text_ru = State()
    start_text_en = State()
    start_media = State()
    current_start_msg = State()
    faq_text_ru = State()
    faq_text_en = State()
    current_faq_msg = State()
    support = State()
    switches = State()


class CommonFunctionsState(StatesGroup):
    find = State()
    user_profile = State()
    select_currency = State()
    refill = State()
    purchase = State()
    input_amount_change_balance = State()
    input_message = State()
    mailing = State()
    mailing_en = State()
    mailing_approve = State()


class PaymentManagementState(StatesGroup):
    cryptobot = State()
    cryptobot_info = State()


class StatisticState(StatesGroup):
    statistic = State()
