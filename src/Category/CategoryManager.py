from datetime import datetime

import discord
from discord.abc import GuildChannel
from sqlalchemy import update

from database.Domain.Category.Entity.Category import Category
from database.Domain.Category.Entity.CategoryGuildMapping import CategoryGuildMapping
from src.Client.Client import Client
from src.Database.DatabaseConnection import getSession
from src.Guild.GuildManager import GuildManager
from src.Logging.Logger import Logger
from src.Types.ClientListenerType import ClientListenerType

logger = Logger("CategoryManager")


class CategoryManager:

    def __init__(self, client: Client, guildManager: GuildManager):
        self.client = client
        self.guildManager = guildManager
        self.session = getSession()

        self.registerListener()

    async def categoryDelete(self, category: GuildChannel):
        """
        Sets the category as deleted in the database

        :param category: Category to delete
        :return:
        """
        if not category.type == discord.ChannelType.category:
            logger.debug(f"Channel {category.name, category.id} is not a category")

            return

        with self.session:
            try:
                updateClause = (update(Category)
                                .where(Category.category_id == category.id)
                                .values(deleted_at=datetime.now()))

                self.session.execute(updateClause)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to delete category {category.name, category.name}", exc_info=error)

                self.session.rollback()
            else:
                logger.debug(f"Category {category.name, category.id} deleted from database")

    async def categoryCreate(self, category: GuildChannel):
        """
        Adds the category to the database

        :param category:
        :return:
        """
        if not category.type == discord.ChannelType.category:
            logger.debug(f"Channel {category.name, category.id} is not a category")

            return

        with self.session:
            try:
                categoryDatabase = Category(
                    category_id=category.id,
                    name=category.name,
                )
                categoryChannelMapping = CategoryGuildMapping(
                    category_id=category.id,
                    guild_id=category.guild.id,
                )

                self.session.add(categoryDatabase)
                self.session.add(categoryChannelMapping)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to add category {category.name, category.id}", exc_info=error)

                self.session.rollback()
            else:
                logger.debug(f"Category {category.name, category.id} added to database")

    async def onBotStart(self):
        pass

    def registerListener(self):
        """
        Register the listeners for the client

        :return:
        """
        self.client.addListener(self.categoryCreate, ClientListenerType.CHANNEL_CREATE)
        self.client.addListener(self.categoryDelete, ClientListenerType.CHANNEL_DELETE)
        self.guildManager.addGuildManagerListener(self.onBotStart)

        logger.debug("Registered listeners to client")
