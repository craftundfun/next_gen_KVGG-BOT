from abc import ABC, abstractmethod

from discord import Guild

from src_bot.Interface.Interface import Interface


class ClientGuildListenerInterface(Interface, ABC):

    @abstractmethod
    async def onGuildUpdate(self, before: Guild, after: Guild):
        pass

    @abstractmethod
    async def onGuildJoin(self, guild: Guild):
        pass

    @abstractmethod
    async def onGuildRemove(self, guild: Guild):
        pass
