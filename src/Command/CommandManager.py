from discord.app_commands import CommandTree

from src.Command.CommandWorker import CommandWorker
from src.Command.PingCommand import PingCommand
from src.Logging.Logger import Logger
from src.Types.ClientListenerType import ClientListenerType

logger = Logger("CommandManager")


class CommandManager:
    """
    Manages all commands and syncs them with the discord API
    """
    tree: CommandTree = None

    def __init__(self, client):
        self.client = client
        self.tree = CommandTree(client)
        self.commandWorker = CommandWorker(client)

        self.commands = []

        self.registerListeners()
        self.addCommands()

    def registerListeners(self):
        self.client.addListener(self.onBotReady, ClientListenerType.READY)

        logger.debug("registered ready listener to Client")

    def addCommands(self):
        # TODO dont hardcode the commands
        command = PingCommand(self.tree)
        self.commands.append(command)
        self.commandWorker.registerListenersAtCommand(command)

    async def syncCommands(self):
        logger.debug("Syncing commands...")
        await self.tree.sync(guild=self.client.get_guild(438689788585967616))
        logger.info("Commands synced")

    async def removeCommands(self):
        self.tree.clear_commands(guild=self.client.get_guild(438689788585967616))

        await self.syncCommands()

    async def onBotReady(self):
        await self.syncCommands()
        # await self.removeCommands()
