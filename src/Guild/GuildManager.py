from discord.guild import Guild as DiscordGuild

from database.Domain.Guild.Entity.Guild import Guild
from database.Domain.Guild.Repository.GuildRepository import GuildRepository
from src.Client.Client import Client
from src.Database.DatabaseConnection import getSession
from src.Logging.Logger import Logger
from src.Types.ClientListenerType import ClientListenerType

logger = Logger("GuildManager")


class GuildManager:

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()

        if not self.session:
            logger.error("No session found")

            exit(1)

        self.guildRepository = GuildRepository(self.session)

        self.registerListeners()

    async def onBotStart(self):
        """
        Traverse all guilds the bot is in and evaluate if they are in the database

        :return:
        """
        for guild in self.client.guilds:
            databaseGuild = self.guildRepository.getGuild(guild)

            if not databaseGuild:
                logger.error(f"Guild {guild.name} not found in database")

                continue

            logger.debug(f"Guild {guild.name} found in database")

            await self.updateGuildOnStart(guild, databaseGuild)

    async def updateGuildOnStart(self, guild: DiscordGuild, databaseGuild: Guild):
        """
        Update the guild if changes are detected

        :param guild:
        :param databaseGuild:
        :return:
        """
        nameBefore = databaseGuild.name
        databaseGuild.name = guild.name

        if nameBefore == guild.name:
            return

        try:
            self.session.add(databaseGuild)
            self.session.commit()
        except Exception as error:
            logger.error(f"Error updating guild name from {nameBefore} to {guild.name}", exc_info=error)
            self.session.rollback()
        else:
            logger.debug(f"Updated guild name from {nameBefore} to {guild.name}")

    async def updateGuild(self, before: DiscordGuild, after: DiscordGuild):
        """
        Update the guild in the database if changes are detected

        :param before:
        :param after:
        :return:
        """
        # TODO
        print(before, after)

    def registerListeners(self):
        self.client.addListener(self.onBotStart, ClientListenerType.READY)
        logger.debug("registered ready listener to Client")

        self.client.addListener(self.updateGuild, ClientListenerType.GUILD_UPDATE)
        logger.debug("registered guild update listener to Client")
