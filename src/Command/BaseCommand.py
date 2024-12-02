from abc import ABC, abstractmethod
from inspect import iscoroutinefunction

from discord.app_commands import CommandTree

from src.Helpers.FunctionName import listenerName
from src.Logging.Logger import Logger
from src.Types.CommandListenerType import CommandListenerType

logger = Logger("BaseCommand")


class BaseCommand(ABC):
    """
    Base class for all commands that are registered in the command tree with listeners
    """
    beforeListener = []
    afterListener = []

    def __init__(self, tree: CommandTree):
        self.tree = tree
        self.register()

    @abstractmethod
    def register(self):
        pass

    def addListener(self, listener: callable, listenerType: CommandListenerType):
        """
        Add a callable (function /) listener

        :param listenerType: Type of listener, for example, before or after
        :param listener: Callable async function
        :return:
        """
        if not iscoroutinefunction(listener):
            logger.error(f"Listener is not an asynchronous function: {listener}")

            raise Exception("Listener must be a coroutine function")

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
