from discord import Client

from src_bot.Command.CommandSkeleton import CommandSkeleton
from src_bot.Interface.Command.CommandSkeletonListenerInterface import CommandSkeletonListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.CommandListenerType import CommandListenerType

logger = Logger("CommandWorker")


class CommandWorker(CommandSkeletonListenerInterface):

    def __init__(self, client: Client):
        self.client = client

    def registerListenersAtCommand(self, command: CommandSkeleton):
        command.addListener(self.beforeCommand, CommandListenerType.BEFORE)
        command.addListener(self.afterCommand, CommandListenerType.AFTER)

    async def beforeCommand(self, **kwargs):
        logger.debug("before command")

    async def afterCommand(self):
        logger.debug("after command")
