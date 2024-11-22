from datetime import datetime

from discord import Guild
from discord.abc import GuildChannel
from sqlalchemy import update

from database.Domain.Channel.Entity.Channel import Channel
from database.Domain.Channel.Entity.ChannelGuildMapping import ChannelGuildMapping
from src.Client.Client import Client
from src.Database.DatabaseConnection import getSession
from src.Guild.GuildManager import GuildManager
from src.Logging.Logger import Logger
from src.Types.ClientListenerType import ClientListenerType

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
        with self.session:
            # IDE can't resolve Channel type
            # noinspection PyUnresolvedReferences
            databaseChannel = Channel(
                channel_id=channel.id,
                name=channel.name,
                type=channel.type.name,
            )
            channelGuildMapping = ChannelGuildMapping(
                channel_id=channel.id,
                guild_id=channel.guild.id
            )

            try:
                self.session.add(databaseChannel)
                self.session.add(channelGuildMapping)
            except Exception as error:
                logger.error(f"Failed to create channel: {error}", exc_info=error)

                self.session.rollback()
            else:
                self.session.commit()

                logger.debug(f"Channel {channel.name, channel.id} created and added to database")

    async def onBotStart(self, guild: Guild):
        """
        Check if all channels are in the database

        :param guild: Guild to check
        :return:
        """
        # TODO maybe optimize this to not call the database for every channel
        # TODO delete channels that are not in the guild anymore
        for channel in guild.channels:
            if not self.session.query(Channel).filter_by(channel_id=channel.id).first():
                logger.debug(f"Channel {channel.name, channel.id} not found in database")
                await self.channelCreate(channel)

        logger.debug(f"Found and added all new channels for guild {guild.name, guild.id}")

    def registerListener(self):
        """
        Register all listeners to corresponding events

        :return:
        """
        self.client.addListener(self.channelDelete, ClientListenerType.CHANNEL_DELETE)
        logger.debug("Channel delete listener registered")

        self.client.addListener(self.channelCreate, ClientListenerType.CHANNEL_CREATE)
        logger.debug("Channel create listener registered")

        self.guildManager.addGuildManagerListener(self.onBotStart)
        logger.debug("Guild manager listener registered")

        logger.info("Channel listeners registered")
