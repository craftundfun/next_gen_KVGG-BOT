from datetime import datetime

from discord.guild import Guild as DiscordGuild
from sqlalchemy import update, null, select
from sqlalchemy.exc import NoResultFound

from database.Domain.models.Guild import Guild
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Helpers.FunctionName import listenerName
from src_bot.Helpers.InterfaceImplementationCheck import checkInterfaceImplementation
from src_bot.Interface.Client.ClientGuildListenerInterface import ClientGuildListenerInterface
from src_bot.Interface.Client.ClientReadyListenerInterface import ClientReadyListenerInterface
from src_bot.Interface.Guild.GuildListenerInterface import GuildListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType
from src_bot.Types.GuildListenerType import GuildListenerType

logger = Logger("GuildManager")


class GuildManager(ClientReadyListenerInterface, ClientGuildListenerInterface):
    startUpGuildCheck = []
    guildJoin = []

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()

        self.registerListeners()

    def addListener(self, listener: callable, type: GuildListenerType):
        """
        Add a listener to the guild manager

        :param listener: Listener to add
        :param type: Type of listener
        :return:
        """
        checkInterfaceImplementation(listener, GuildListenerInterface)

        match type:
            case GuildListenerType.GUILD_JOIN:
                self.guildJoin.append(listener)
            case GuildListenerType.START_UP:
                self.startUpGuildCheck.append(listener)
            case _:
                logger.error(f"Invalid listener type: {type}")

        logger.debug(f"Listener successfully added: {listenerName(listener)}")

    # TODO look for changes in existing guilds while bot was offline
    async def onBotReady(self):
        """
        Traverse all guilds the bot is in and evaluate if they are in the database

        :return:
        """
        with self.session:
            for guild in self.client.guilds:
                selectQuery = select(Guild).where(Guild.guild_id == guild.id)

                try:
                    databaseGuild = self.session.scalars(selectQuery).one()
                except NoResultFound:
                    # TODO maybe in a extra function, we are doing this twice
                    databaseGuild = Guild(
                        guild_id=guild.id,
                        name=guild.name,
                        joined_at=datetime.now(),
                        icon=guild.icon.url if guild.icon else None,
                    )

                    self.session.add(databaseGuild)
                    self.session.commit()
                except Exception as error:
                    logger.error(f"Failed to get guild {guild.name, guild.id}", exc_info=error)

                    continue

                logger.debug(f"Guild {guild.name, guild.id} found in database")

                await self.updateGuildOnStart(guild, databaseGuild)

                for listener in self.startUpGuildCheck:
                    await listener(guild)

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

    async def onGuildUpdate(self, before: DiscordGuild, after: DiscordGuild):
        """
        Update the guild in the database if changes are detected

        :param before:
        :param after:
        :return:
        """
        # TODO
        print(before, after)

    async def onGuildJoin(self, guild: DiscordGuild):
        """
        Add the guild to the database or renew it

        :param guild: Guild to add or renew
        :return:
        """
        with self.session:
            selectQuery = select(Guild).where(Guild.guild_id == guild.id)

            try:
                databaseGuild = self.session.scalars(selectQuery).one()
            except NoResultFound:
                databaseGuild = Guild(
                    guild_id=guild.id,
                    name=guild.name,
                    joined_at=datetime.now(),
                    icon=guild.icon.url if guild.icon else None,
                )

                self.session.add(databaseGuild)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to get or create guild {guild.name, guild.id}", exc_info=error)

                return

            logger.debug(f"Guild {guild.name, guild.id} already in database")

            # renew the guild in the database
            databaseGuild.joined_at = datetime.now()

            try:
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to update guild {guild.name, guild.id}", exc_info=error)
                self.session.rollback()

        for listener in self.guildJoin:
            await listener(guild)

    async def onGuildRemove(self, guild: DiscordGuild):
        """
        When the bot leaves a guild, update the guild in the database

        :param guild: Guild to update
        :return:
        """
        with self.session:
            updateClause = (update(Guild)
                            .where(Guild.guild_id == guild.id)
                            .values(joined_at=null()))

            try:
                self.session.execute(updateClause)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to update guild {guild.name, guild.id}", exc_info=error)
                self.session.rollback()
            else:
                logger.debug(f"Updated guild {guild.name, guild.id} after leave")

    def registerListeners(self):
        """
        Register all listeners to corresponding events

        :return:
        """
        self.client.addListener(self.onBotReady, ClientListenerType.READY)
        logger.debug("Registered ready listener to Client")

        self.client.addListener(self.onGuildUpdate, ClientListenerType.GUILD_UPDATE)
        logger.debug("Registered guild update listener to Client")

        self.client.addListener(self.onGuildJoin, ClientListenerType.GUILD_JOIN)
        logger.debug("Registered guild join listener to Client")

        self.client.addListener(self.onGuildRemove, ClientListenerType.GUILD_REMOVE)
        logger.debug("Registered guild remove listener to Client")
