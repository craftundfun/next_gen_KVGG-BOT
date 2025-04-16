from abc import ABC, abstractmethod

from discord import Guild

from src_bot.Interface.Interface import Interface


class GuildListenerInterface(Interface, ABC):

    @abstractmethod
    async def onGuildJoin(self, guild: Guild):
        pass

    @abstractmethod
    async def onGuildStartupCheck(self, guild: Guild):
        pass
