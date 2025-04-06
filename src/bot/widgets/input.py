from __future__ import annotations

from collections.abc import Callable
from decimal import InvalidOperation, Decimal
from typing import (
    Any,
    Generic,
    Optional,
    Union,
)

from aiogram.dispatcher.event.handler import FilterObject
from aiogram.types import ContentType, Message
from aiogram_dialog.api.protocols import DialogManager, DialogProtocol
from aiogram_dialog.widgets.input import BaseInput
from aiogram_dialog.widgets.input.text import TypeFactory, OnSuccess, OnError, ManagedTextInput, T
from aiogram_dialog.widgets.widget_event import (
    WidgetEventProcessor,
    ensure_event_processor,
)


class TextInputDecimal(BaseInput, Generic[T]):
    def __init__(
            self,
            id: str,
            on_success: Union[OnSuccess[T], WidgetEventProcessor, None] = None,
            on_error: Union[OnError, WidgetEventProcessor, None] = None,
            filter: Optional[Callable[..., Any]] = None,
    ):
        super().__init__(id=id)
        if filter is not None:
            self.filter = FilterObject(filter)
        else:
            self.filter = None
        self.type_factory = Decimal
        self.on_success = ensure_event_processor(on_success)
        self.on_error = ensure_event_processor(on_error)

    async def process_message(
            self,
            message: Message,
            dialog: DialogProtocol,
            manager: DialogManager,
    ) -> bool:
        if message.content_type != ContentType.TEXT:
            return False
        if self.filter and not await self.filter.call(
                manager.event, **manager.middleware_data,
        ):
            return False
        try:
            input = message.text
            if ',' in input:
                input = message.text.replace(',', '.')
            value = self.type_factory(input)
        except InvalidOperation as err:
            await self.on_error.process_event(
                message, self.managed(manager), manager, err,
            )
        else:
            # store original text
            self.set_widget_data(manager, message.text)
            await self.on_success.process_event(
                message, self.managed(manager), manager, value,
            )
        return True

    def get_value(self, manager: DialogManager) -> Optional[T]:
        data = self.get_widget_data(manager, None)
        if data is None:
            return None
        return self.type_factory(data)

    def managed(self, manager: DialogManager):
        return ManagedTextInput(self, manager)
