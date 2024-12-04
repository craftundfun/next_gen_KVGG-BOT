from datetime import datetime

import discord
from discord import Guild
from discord.abc import GuildChannel
from sqlalchemy import update, text, select

from database.Domain.models.Channel import Channel
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Guild.GuildManager import GuildManager
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType
from src_bot.Types.GuildListenerType import GuildListenerType

logger = Logger("ChannelManager")


class ChannelManager:

    def __init__(self, client: Client, guildManager: GuildManager):
        self.client = client
        self.guildManager = guildManager
        self.session = getSession()

        self.registerListener()

    async def channelDelete(self, channel: GuildChannel):
        """
        Sets the channel as deleted in the database

        :param channel: GuildChannel to delete
        :return:
        """
        if channel.type == discord.ChannelType.category:
            logger.debug(f"Channel {channel.name, channel.id} is a category")

            return

        with self.session:
            updateClause = (update(Channel)
                            .where(Channel.channel_id == channel.id)
                            .values(deleted_at=datetime.now()))

            try:
                self.session.execute(updateClause)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to delete channel: {error}", exc_info=error)
            else:
                logger.debug(f"Channel {channel.name, channel.id} deleted from database")

    async def channelCreate(self, channel: GuildChannel):
        """
        Adds the channel to the database

        :param channel: GuildChannel to add
        :return:
        """
        if channel.type == discord.ChannelType.category:
            logger.debug(f"Channel {channel.name, channel.id} is a category")

            return

        with self.session:
            # IDE can't resolve Channel type
            # noinspection PyUnresolvedReferences
            databaseChannel = Channel(
                channel_id=channel.id,
                name=channel.name,
                type=channel.type.name,
                guild_id=channel.guild.id
            )

            try:
                self.session.add(databaseChannel)
                self.session.commit()

                logger.debug(f"Channel {channel.name, channel.id} created and added to database")
            except Exception as error:
                logger.error(f"Failed to create channel: {error}", exc_info=error)

                self.session.rollback()

    async def _findMissingChannels(self, guild: Guild):
        """
        Find missing channels in the database if some got created while the bot was offline

        :param guild: Guild to check
        :return:
        """
        channelIdsAsTEXT = ", ".join([f"({str(channel.id)})"
                                      for channel in guild.channels if channel.type != discord.ChannelType.category])
        # call database routine
        sql = text("CALL FindMissingChannels(:channelIds, @missing_channels);")

        with self.session:
            try:
                self.session.execute(sql, {"channelIds": channelIdsAsTEXT})
                result = self.session.execute(text("SELECT @missing_channels;")).fetchall()

                # [(None,)] possible result if the procedure found nothing
                if not result or not result[0][0]:
                    logger.debug(f"No missing channels found for {guild.name, guild.id}")

                    return

                # extract the string inside the parentheses and split by commas
                # removing the parentheses
                channelIDsStr = result[0][0][1:-1]
                # convert each item to an integer
                missingChannelIDs = list(map(int, channelIDsStr.split(',')))
            except Exception as error:
                logger.error(f"Failed to find missing channels: {error}", exc_info=error)

                return

        for id in missingChannelIDs:
            try:
                channel = await self.client.fetch_channel(id)

                if not channel:
                    logger.error(f"Channel {id} not found in guild {guild.name, guild.id}")

                    continue
            except Exception as error:
                logger.error(f"Failed to fetch channel from {guild.name, guild.id}", exc_info=error)

                continue
            else:
                await self.channelCreate(channel)

        logger.debug(f"Found and added all new channels for guild {guild.name, guild.id}")

    async def _findDeletedChannels(self, guild: Guild):
        """
        Set channels as deleted in the database if they are not in the guild anymore

        :param guild: Guild to check
        :return:
        """
        with self.session:
            try:
                selectClause = (select(Channel)
                                .where(Channel.guild_id == guild.id))
                guildChannels = self.session.execute(selectClause).scalars().all()

                for channel in guildChannels:
                    if channel.channel_id not in [guildChannel.id for guildChannel in guild.channels]:
                        channel.deleted_at = datetime.now()

                self.session.commit()

                logger.debug(f"Deleted channels updated for guild {guild.name, guild.id}")
            except Exception as error:
                logger.error(f"Failed to find deleted channels for guild {guild.name, guild.id}", exc_info=error)

    async def onBotStart(self, guild: Guild):
        """
        Check if all channels are in the database

        :param guild: Guild to check
        :return:
        """
        await self._findMissingChannels(guild)
        await self._findDeletedChannels(guild)

    """
    # TODO same functions here, remove if they dont change
    """

    async def onGuildJoin(self, guild: Guild):
        """
        Check if all channels are in the database

        :param guild: Guild to check
        :return:
        """
        await self._findMissingChannels(guild)
        await self._findDeletedChannels(guild)

    async def updateChannel(self, before: GuildChannel, after: GuildChannel):
        # TODO

        pass

    def registerListener(self):
        """
        Register all listeners to corresponding events

        :return:
        """
        self.client.addListener(self.channelDelete, ClientListenerType.CHANNEL_DELETE)
        logger.debug("Channel delete listener registered")

        self.client.addListener(self.channelCreate, ClientListenerType.CHANNEL_CREATE)
        logger.debug("Channel create listener registered")

        self.guildManager.addGuildManagerListener(self.onBotStart, GuildListenerType.START_UP)
        logger.debug("Guild manager listener registered")

        self.guildManager.addGuildManagerListener(self.onGuildJoin, GuildListenerType.GUILD_JOIN)
        logger.debug("Guild join listener registered")

        logger.info("Channel listeners registered")
