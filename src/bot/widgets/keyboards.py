from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram_dialog import DialogProtocol, ShowMode
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.widget_event import ensure_event_processor

OnClick = Callable[[CallbackQuery, "Button", DialogManager], Awaitable]


class Refresh(Keyboard):
    def __init__(self,
                 text: Text,
                 id: str = 'refresh',
                 when: WhenCondition = None
                 ):
        super().__init__(id=id, when=when)
        self.text = text
        self.on_click_handler = ensure_event_processor(self.default_on_click)

    @staticmethod
    async def default_on_click(event: CallbackQuery, widget: Any, dialog_manager: DialogManager):
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND

    async def _process_own_callback(
            self,
            callback: CallbackQuery,
            dialog: DialogProtocol,
            manager: DialogManager,
    ) -> bool:
        await self.on_click_handler.process_event(callback, self, manager)
        return True

    async def _render_keyboard(
            self,
            data: dict,
            manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                InlineKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    callback_data=self._own_callback_data(),
                ),
            ],
        ]
