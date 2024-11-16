from typing import Any

from discord import Client as discordClient
from discord import Intents


class Client(discordClient):
    _self = None


    def __new__(cls, *args, **kwargs) -> "Client":
        if not cls._self:
            cls._self = super().__new__(cls)

        return cls._self

    def __init__(self, controller, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)

        self.controller = controller

    async def on_ready(self):
        await self.controller.botReady()
