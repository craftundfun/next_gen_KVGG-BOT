from os import environ

from discord import Intents

from src.Category.CategoryManager import CategoryManager
from src.Channel.ChannelManager import ChannelManager
from src.Client.Client import Client
from src.Command.CommandManager import CommandManager
from src.Guild.GuildManager import GuildManager
from src.Logging.Logger import Logger

logger = Logger("Controller")


class Controller:

    def __init__(self):
        self.token = environ.get("DISCORD_TOKEN")

        if not self.token:
            logger.error("No token found in .env file")

            exit(1)

        self.client = Client(self, intents=Intents.all())
        self.commandManager = CommandManager(self.client)
        self.guildManager = GuildManager(self.client)
        self.channelManager = ChannelManager(self.client, self.guildManager)
        self.categoryManager = CategoryManager(self.client, self.guildManager)

        self.registerListeners()

    def registerListeners(self):
        pass

    def run(self):
        try:
            self.client.run(self.token, reconnect=True)
        except Exception as error:
            logger.error("Error while running client", exc_info=error)

            exit(1)
