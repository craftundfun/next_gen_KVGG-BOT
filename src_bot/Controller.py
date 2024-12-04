from os import environ

from discord import Intents

from src_bot.Category.CategoryManager import CategoryManager
from src_bot.Channel.ChannelManager import ChannelManager
from src_bot.Client.Client import Client
from src_bot.Command.CommandManager import CommandManager
from src_bot.Guild.GuildManager import GuildManager
from src_bot.Logging.Logger import Logger
from src_bot.Member.MemberManager import MemberManager

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
        self.memberManager = MemberManager(self.client)

        self.registerListeners()

    def registerListeners(self):
        pass

    def run(self):
        try:
            self.client.run(self.token, reconnect=True)
        except Exception as error:
            logger.error("Error while running client", exc_info=error)

            exit(1)
