from aiogram.fsm.state import StatesGroup, State


class ProfileState(StatesGroup):
    profile = State()
    purchases = State()
    purchase_details = State()
    ch_cur = State()
    ch_lg = State()


class RefillState(StatesGroup):
    refill = State()
    select_payment_method = State()
    invoice = State()


class InvoiceState(StatesGroup):
    invoice = State()
    enter_code = State()

class SettingsState(StatesGroup):
    settings = State()
    ch_lg = State()
    ch_cur = State()


class FaqState(StatesGroup):
    faq = State()


class SupportState(StatesGroup):
    support = State()


class ShoppingState(StatesGroup):
    select_category = State()
    select_position = State()
    position_details = State()
    input_amount_item = State()
    not_enough_money = State()
    approve_buy = State()
    receipt = State()