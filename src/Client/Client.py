from inspect import iscoroutinefunction
from typing import Any

from discord import Client as discordClient, Guild
from discord import Intents
from discord.abc import GuildChannel

from src.Helpers.FunctionName import listenerName
from src.Logging.Logger import Logger
from src.Types.ClientListenerType import ClientListenerType

logger = Logger("Client")


class Client(discordClient):
    _self = None
    readyListener = []
    guildUpdate = []
    channelCreateListener = []
    channelDeleteListener = []

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
        if not iscoroutinefunction(listener):
            logger.error(f"Listener is not an asynchronous function: {listener}")

            raise ValueError(f"Listener is not async")

        match listenerType:
            case ClientListenerType.READY:
                self.readyListener.append(listener)
            case ClientListenerType.GUILD_UPDATE:
                self.guildUpdate.append(listener)
            case ClientListenerType.CHANNEL_CREATE:
                self.channelCreateListener.append(listener)
            case ClientListenerType.CHANNEL_DELETE:
                self.channelDeleteListener.append(listener)
            case _:
                logger.error(f"Invalid listener type: {listenerType}")

                raise ValueError(f"Invalid listener type: {listenerType}")

        logger.debug(f"Listener successfully added: {listenerName(listener)}")

    async def on_ready(self):
        """
        Notify all listeners that the bot is ready

        :return:
        """
        for listener in self.readyListener:
            await listener()
            logger.debug(f"Notified ready listener: {listenerName(listener)}")

    async def on_guild_update(self, before: Guild, after: Guild):
        """
        Notify all listeners that a guild has been updated

        :param before: State before the change
        :param after: State after the change
        :return:
        """
        for listener in self.guildUpdate:
            await listener(before, after)
            logger.debug(f"Notified guild update listener: {listenerName(listener)}")

    async def on_guild_channel_create(self, channel: GuildChannel):
        """
        Notify all listeners that a channel has been created

        :param channel: Channel that was created
        :return:
        """
        for listener in self.channelCreateListener:
            await listener(channel)
            logger.debug(f"Notified channel create listener: {listenerName(listener)}")

    async def on_guild_channel_delete(self, channel: GuildChannel):
        """
        Notify all listeners that a channel has been deleted

        :param channel: Channel that was deleted
        :return:
        """
        for listener in self.channelDeleteListener:
            await listener(channel)
            logger.debug(f"Notified channel delete listener: {listenerName(listener)}")
