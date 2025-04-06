from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Case, Format

from src.bot.dialogs.admins.settings.callable import on_start_media, \
    on_media_skip, on_start_message_input, on_input_faq_text_ru, on_input_faq_text_en, on_input_support, on_switches
from src.bot.dialogs.admins.settings.getter import change_data_getter, input_start_text_ru_getter, current_msg_getter, \
    input_faq_text_ru_getter, current_faq_msg_getter, switches_getter
from src.bot.states import SettingsState
from src.bot.widgets import GetText

change_data = Window(
    GetText(
        'change-data'
    ),

    Row(
        Button(
            GetText('change-data.faq-btn'),
            id='faq_btn',
        ),
        SwitchTo(
            Case(
                {
                    True: GetText('change-data.mounted'),
                    ...: GetText('change-data.unmounted')
                },
                selector=lambda data, widget, manager: bool(data['faq_text_ru']) and bool(data['faq_text_en'])
            ),
            state=SettingsState.faq_text_ru,
            id='faq_change_btn'
        )
    ),
    Row(
        Button(
            GetText('change-data.start-message-btn'),
            id='start_msg'
        ),
        SwitchTo(
            Case(
                {
                    True: GetText('change-data.mounted'),
                    ...: GetText('change-data.unmounted')
                },
                selector=lambda data, widget, manager: bool(data['start_text_ru']) and bool(data['start_text_en'])
            ),
            state=SettingsState.start_text_ru,
            id='start_change_btn'
        )
    ),
    Row(
        Button(
            GetText('change-data.support-btn'),
            id='support_btn'
        ),
        SwitchTo(
            Case(
                {
                    True: Format('✅ @{support}'),
                    ...: GetText('change-data.unmounted'),
                },
                selector=lambda data, widget, manager: bool(data['support'])
            ),
            state=SettingsState.support,
            id='support_change_btn'
        )
    ),

    Row(
        Button(
            GetText('change-data.category-without-items-btn'),
            id='category_without_items_btn'
        ),
        Button(
            Case(
                {
                    True: GetText('change-data.showed'),
                    ...: GetText('change-data.unshowed')
                },
                selector=lambda data, widget, manager: bool(data['category_without_items'])
            ),
            on_click=on_switches,
            id='category_without_items'
        )
    ),

    Row(
        Button(
            GetText('change-data.position-without-items-btn'),
            id='position_btn'
        ),
        Button(
            Case(
                {
                    True: GetText('change-data.showed'),
                    ...: GetText('change-data.unshowed')
                },
                selector=lambda data, widget, manager: bool(data['position_without_items'])
            ),
            on_click=on_switches,
            id='position_without_items'
        )
    ),

    getter=change_data_getter,
    state=SettingsState.change_data
)

input_start_text_ru = Window(
    GetText(
        'input-start-text'
    ),
    TextInput(
        on_success=on_start_message_input,
        id='ru'
    ),

    SwitchTo(
        GetText(
            'input-start-text.current-msg-btn'
        ),
        state=SettingsState.current_start_msg,
        id='to_current_start_msg',
        when=(F['start_text_ru'].is_not(None)) & (F['start_text_en'].is_not(None))
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=SettingsState.change_data,
        id='back'
    ),
    getter=input_start_text_ru_getter,
    state=SettingsState.start_text_ru
)

input_start_text_en = Window(
    GetText(
        'input-start-text.en'
    ),
    TextInput(
        on_success=on_start_message_input,
        id='en'
    ),
    SwitchTo(
        GetText(
            'back'
        ),
        state=SettingsState.start_text_ru,
        id='back'
    ),
    state=SettingsState.start_text_en
)

input_start_text_media = Window(
    GetText(
        'input-start-text.media'
    ),

    MessageInput(
        func=on_start_media,
        content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION]
    ),

    Button(
        GetText(
            'skip'
        ),
        on_click=on_media_skip,
        id='on_media_skip'
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=SettingsState.start_text_en,
        id='back'
    ),

    state=SettingsState.start_media
)

current_msg = Window(
    GetText(
        'current-start-msg'
    ),

    DynamicMedia(
        'media',
        when=F['media']
    ),

    SwitchTo(
        GetText('back'),
        id='bck',
        state=SettingsState.start_text_ru
    ),
    getter=current_msg_getter,
    state=SettingsState.current_start_msg
)

input_faq_text_ru = Window(
    GetText(
        'input-faq-text'
    ),

    TextInput(
        on_success=on_input_faq_text_ru,
        id='on_faq_ru'
    ),

    SwitchTo(
        GetText('input-faq-text.current-msg-btn'),
        state=SettingsState.current_faq_msg,
        id='current_msg',
        when=(F['faq_text_ru']) & (F['faq_text_en'])
    ),

    SwitchTo(
        GetText('back'),
        state=SettingsState.change_data,
        id='cbk'
    ),
    getter=input_faq_text_ru_getter,
    state=SettingsState.faq_text_ru
)

input_faq_text_en = Window(
    GetText(
        'input-faq-text.en'
    ),

    TextInput(
        on_success=on_input_faq_text_en,
        id='on_faq_en'
    ),

    SwitchTo(
        GetText('back'),
        state=SettingsState.faq_text_ru,
        id='cbk'
    ),
    state=SettingsState.faq_text_en
)

current_faq_msg = Window(
    GetText(
        'current-faq-msg'
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        id='cbk',
        state=SettingsState.faq_text_ru
    ),
    getter=current_faq_msg_getter,
    state=SettingsState.current_faq_msg
)

input_support = Window(
    GetText(
        'input-support'
    ),

    TextInput(
        id='support',
        on_success=on_input_support
    ),

    SwitchTo(
        GetText(
            'back'
        ),
        state=SettingsState.change_data,
        id='bck'
    ),

    state=SettingsState.support
)

##### SWITCHES ######

switches = Window(
    GetText(
        'switches'
    ),

    Row(
        Button(
            GetText(
                'switches.work-btn'
            ),
            id='work_btn'
        ),

        Button(
            Case(
                {
                    True: GetText('switches.status-on-btn'),
                    ...: GetText('switches.status-off-btn')
                },
                selector=lambda data, widget, manger: data['status_work']
            ),
            on_click=on_switches,
            id='status_work'
        )

    ),

    Row(
        Button(
            GetText(
                'switches.refill-btn'
            ),
            id='refill_btn'
        ),
        Button(
            Case(
                {
                    True: GetText('switches.status-on-btn'),
                    ...: GetText('switches.status-off-btn')
                },
                selector=lambda data, widget, manger: data['status_refill']
            ),
            on_click=on_switches,
            id='status_refill'
        )
    ),
    Row(
        Button(
            GetText(
                'switches.purchases-btn'
            ),
            id='purchases_btn'
        ),
        Button(
            Case(
                {
                    True: GetText('switches.status-on-btn'),
                    ...: GetText('switches.status-off-btn')
                },
                selector=lambda data, widget, manger: data['status_buy']
            ),
            on_click=on_switches,
            id='status_buy'
        )
    ),

    state=SettingsState.switches,
    getter=switches_getter
)
