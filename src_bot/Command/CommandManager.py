from discord.app_commands import CommandTree
import discord
from src_bot.Client.Client import Client
from src_bot.Command.CommandWorker import CommandWorker
from src_bot.Command.Commands.PingCommand import PingCommand
from src_bot.Logging.Logger import Logger
from src_bot.Translator.Translator import Translator
from src_bot.Types.ClientListenerType import ClientListenerType

logger = Logger("CommandManager")


class CommandManager:
    """
    Manages all commands and syncs them with the discord API
    """
    tree: CommandTree = None
    guilds: list[discord.Object] = None

    def __init__(self, client: Client):
        self.client = client

        self.tree = CommandTree(client)
        self.commandWorker = CommandWorker(client)
        self.translator = Translator()

        self.commands = []

        self.registerListeners()

    def registerListeners(self):
        self.client.addListener(self.onBotReady, ClientListenerType.READY)

        logger.debug("Registered ready listener to Client")

    def addCommands(self, guilds: list[discord.Object]):
        # TODO dont hardcode the commands
        command = PingCommand(self.tree, guilds)
        self.commands.append(command)
        self.commandWorker.registerListenersAtCommand(command)

    async def syncCommands(self):
        self.addCommands(self.guilds)

        logger.debug("Syncing commands...")
        print(self.guilds)
        for guild in self.guilds:
            await self.tree.sync(guild=guild)
        logger.info("Commands synced")

    async def removeCommands(self):
        for guild in self.guilds:
            self.tree.clear_commands(guild=guild)
            await self.tree.sync(guild=guild)

        # await self.syncCommands()

    async def onBotReady(self):
        # TODO dont hardcode the guilds and use settings from database
        # fill guilds here , otherwise the client cant fetch the guilds
        self.guilds = [discord.Object(id=guild.id) for guild in self.client.guilds]

        await self.translator.load()
        await self.tree.set_translator(self.translator)
        logger.debug("Translator loaded and set")

        # await self.syncCommands()
        await self.removeCommands()

        logger.error("Commands synced or removed")

        pass
