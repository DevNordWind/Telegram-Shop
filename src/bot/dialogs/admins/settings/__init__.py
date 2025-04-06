from aiogram_dialog import Dialog

from .window import (
    change_data,
    input_start_text_ru,
    input_start_text_en,
    input_start_text_media,
    current_msg,
    input_faq_text_ru,
    input_faq_text_en,
    current_faq_msg,
    input_support,
    switches
)

settings_dialog = Dialog(
    change_data,
    input_start_text_ru,
    input_start_text_en,
    input_start_text_media,
    current_msg,
    input_faq_text_ru,
    input_faq_text_en,
    current_faq_msg,
    input_support,
    switches
)
