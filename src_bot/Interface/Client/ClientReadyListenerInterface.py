from abc import ABC, abstractmethod

from src_bot.Interface.Interface import Interface


class ClientReadyListenerInterface(Interface, ABC):

    @abstractmethod
    async def onBotReady(self):
        pass
