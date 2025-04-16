from abc import ABC, abstractmethod

from discord.abc import GuildChannel

from src_bot.Interface.Interface import Interface


class ClientChannelListenerInterface(Interface, ABC):

    @abstractmethod
    async def onGuildChannelCreate(self, channel: GuildChannel):
        pass

    @abstractmethod
    async def onGuildChannelDelete(self, channel: GuildChannel):
        pass

    @abstractmethod
    async def onGuildChannelUpdate(self, before: GuildChannel, after: GuildChannel):
        pass
