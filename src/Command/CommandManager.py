from discord.app_commands import CommandTree

from src.Command.CommandWorker import CommandWorker
from src.Command.PingCommand import PingBaseCommand
from src.Types.ClientListenerType import ClientListenerType
from src.Types.CommandListenerType import CommandListenerType


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

    def addCommands(self):
        # TODO dont hardcode the commands
        command = PingBaseCommand(self.tree)
        self.commands.append(command)
        command.addListener(self.commandWorker.prepareCommand, CommandListenerType.BEFORE)
        command.addListener(self.commandWorker.afterCommand, CommandListenerType.AFTER)

    async def syncCommands(self):
        await self.tree.sync(guild=self.client.get_guild(438689788585967616))

    async def removeCommands(self):
        self.tree.clear_commands(guild=self.client.get_guild(438689788585967616))

        await self.tree.sync(guild=self.client.get_guild(438689788585967616))

    async def onBotReady(self):
        print("Syncing commands...")
        # await self.syncCommands()
        print("Bot is ready and commands are synced")

        await self.removeCommands()
