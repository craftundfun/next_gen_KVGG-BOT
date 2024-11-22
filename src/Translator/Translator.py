import json
from typing import Optional

import discord.app_commands
from discord import Locale
from discord.app_commands import locale_str, TranslationContextTypes

from src.Logging.Logger import Logger

logger = Logger("Translator")


class Translator(discord.app_commands.Translator):
    en: dict = {}
    de: dict = {}

    def __init__(self):
        super().__init__()

    async def load(self) -> None:
        with open("locales/en.json", "r") as file:
            self.en = json.load(file)

        with open("locales/de.json", "r") as file:
            self.de = json.load(file)

    async def unload(self) -> None:
        self.en = {}
        self.de = {}

    async def translate(self,
                        string: locale_str,
                        locale: Locale,
                        context: TranslationContextTypes) -> Optional[str]:
        def getTranslation(dictToUse: dict) -> str:
            try:
                translation = dictToUse.get(str(string))

                if not translation:
                    raise KeyError(f"No translation for {string} in language {locale}")

                logger.debug(f"Translated {string} to {locale}")

                return translation
            except KeyError as error:
                logger.error(f"No translation for {string} in language {locale}", exc_info=error)

                # Fallback to input
                return str(string)

        match locale:
            case Locale.american_english | Locale.british_english:
                return getTranslation(self.en)
            case Locale.german:
                return getTranslation(self.de)
            case _:
                return getTranslation(self.en)
