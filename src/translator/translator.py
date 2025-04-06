import os
from typing import Set

from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator


class Translator:
    t_hub: TranslatorHub

    def __init__(self):
        self.path = './texts'
        self.t_hub = TranslatorHub(
            root_locale='RU',
            locales_map={
                "RU": ("RU", "EN"),
                "EN": ("EN", "RU"),
            },
            translators=[
                FluentTranslator(
                    locale='RU',
                    translator=FluentBundle.from_files(
                        "RU-RU",
                        filenames=self.get_files('RU'),
                        use_isolating=False
                    ),

                ),
                FluentTranslator(
                    locale='EN',
                    translator=FluentBundle.from_files(
                        locale="EN-US",
                        filenames=self.get_files("EN"),
                        use_isolating=False
                    )
                ),
            ]
        )

    def get_files(self, locale: str) -> list[str]:
        ftl_files = []
        path = self.path + '/' + locale
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.ftl'):
                    ftl_files.append(os.path.join(root, file))
        return ftl_files

    def get_all_texts(self, key: str, **kwargs) -> set[str]:
        return {self.t_hub.get_translator_by_locale(locale).get(key, **kwargs) for locale in
                self.t_hub.translators_map.keys()}
