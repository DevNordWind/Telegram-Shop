from aiogram.filters import Filter
from aiogram.types import Message
from fluentogram import TranslatorRunner


class TranslatorFilter(Filter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, event: Message, translator: TranslatorRunner) -> bool:
        return translator.get(self.key) == event.text
