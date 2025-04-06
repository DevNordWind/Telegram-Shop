from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from fluentogram import TranslatorRunner


class GetText(Text):
    """This class produced by Translator"""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data: dict, manager: DialogManager, **kwargs) -> str:
        translator: TranslatorRunner = manager.middleware_data['translator']
        return str(translator.get(self.key, **data))
