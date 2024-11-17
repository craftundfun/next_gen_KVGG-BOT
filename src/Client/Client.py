from inspect import iscoroutinefunction
from typing import Any

from discord import Client as discordClient
from discord import Intents

from src.Types.ClientListenerType import ClientListenerType


class Client(discordClient):
    _self = None
    readyListener = []

    def __new__(cls, *args, **kwargs) -> "Client":
        if not cls._self:
            cls._self = super().__new__(cls)

        return cls._self

    def __init__(self, controller, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)

        self.controller = controller

    def addListener(self, listener: callable, listenerType: ClientListenerType):
        """
        Add a callable (function /) listener to a specific event

        :param listener: Callable async function
        :param listenerType: Type
        :return:
        """
        print("Hey")

        if not iscoroutinefunction(listener):
            raise ValueError(f"Listener is not async")

        match listenerType:
            case ClientListenerType.READY:
                self.readyListener.append(listener)
            case _:
                raise ValueError(f"Invalid listener type: {listenerType}")

        print("Listener successfully added")

    async def on_ready(self):
        print("Bot is ready in Client class")
        print("Listener: ", self.readyListener)

        for listener in self.readyListener:
            print("before listener")
            await listener()
            print("after listener")
