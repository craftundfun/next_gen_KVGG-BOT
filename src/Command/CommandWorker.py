from discord import Client

from src.Command.BaseCommand import BaseCommand
from src.Logging.Logger import Logger
from src.Types.CommandListenerType import CommandListenerType

logger = Logger("CommandWorker")


class CommandWorker:

    def __init__(self, client: Client):
        self.client = client

    def registerListenersAtCommand(self, command: BaseCommand):
        command.addListener(self.prepareCommand, CommandListenerType.BEFORE)
        command.addListener(self.afterCommand, CommandListenerType.AFTER)

    async def prepareCommand(self, **kwargs):
        logger.debug("before command")

    async def afterCommand(self):
        logger.debug("after command")
