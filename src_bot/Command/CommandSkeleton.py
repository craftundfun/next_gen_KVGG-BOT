from abc import ABC, abstractmethod

import discord.object
from discord.app_commands import CommandTree

from src_bot.Helpers.FunctionName import listenerName
from src_bot.Helpers.InterfaceImplementationCheck import checkInterfaceImplementation
from src_bot.Interface.Command.CommandSkeletonListenerInterface import CommandSkeletonListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.CommandListenerType import CommandListenerType

logger = Logger("CommandSkeleton")


class CommandSkeleton(ABC):
    """
    Base class for all commands that are registered in the command tree with listeners
    """
    beforeListener = []
    afterListener = []

    def __init__(self, tree: CommandTree, guilds: list[discord.object.Object]):
        self.tree = tree
        self.guilds = guilds

        self.registerCommand()

    @abstractmethod
    def registerCommand(self):
        pass

    def addListener(self, listener: callable, listenerType: CommandListenerType):
        """
        Add a callable (function /) listener

        :param listenerType: Type of listener, for example, before or after
        :param listener:  a callable async function
        :return:
        """
        checkInterfaceImplementation(listener, CommandSkeletonListenerInterface)

        match listenerType:
            case CommandListenerType.BEFORE:
                self.beforeListener.append(listener)
            case CommandListenerType.AFTER:
                self.afterListener.append(listener)
            case _:
                logger.error(f"Invalid listener type: {listenerType}")

                raise ValueError(f"Invalid listener type: {listenerType}")

    async def notifyBefore(self):
        """
        Notify all before listeners before the command has been executed

        :return:
        """
        for listener in self.beforeListener:
            await listener()
            logger.debug(f"notified before listener: {listenerName(listener)}")

    async def notifyAfter(self):
        """
        Notify all after listeners after the command has been executed

        :return:
        """
        for listener in self.afterListener:
            await listener()
            logger.debug(f"notified after listener: {listenerName(listener)}")
