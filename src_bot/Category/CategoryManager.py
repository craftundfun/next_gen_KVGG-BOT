from datetime import datetime

import discord
from discord import Guild
from discord.abc import GuildChannel
from sqlalchemy import update, text, select

from database.Domain.models.Category import Category
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Guild.GuildManager import GuildManager
from src_bot.Interface.Client.ClientChannelListenerInterface import ClientChannelListenerInterface
from src_bot.Interface.Guild.GuildListenerInterface import GuildListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType
from src_bot.Types.GuildListenerType import GuildListenerType

logger = Logger("CategoryManager")


class CategoryManager(ClientChannelListenerInterface, GuildListenerInterface):

    def __init__(self, client: Client, guildManager: GuildManager):
        self.client = client
        self.guildManager = guildManager
        self.session = getSession()

        self.registerListener()

    async def onGuildChannelDelete(self, category: GuildChannel):
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

    async def onGuildChannelCreate(self, category: GuildChannel):
        """
        Checks if the given channel is a category and invokes the category creation

        :param category: Category to create
        """
        if not category.type == discord.ChannelType.category:
            logger.debug(f"Channel {category.name, category.id} is not a category")

            return

        await self._createCategories([category])

    async def _createCategories(self, categories: list[GuildChannel]):
        """
        Adds the categories to the database

        :param categories: Categories to add
        :return:
        """
        if len(categories) == 0:
            logger.debug("No categories to create")

            return

        categoryDatabaseObjects = []

        for category in categories:
            categoryDatabase = Category(
                category_id=category.id,
                name=category.name,
                guild_id=category.guild.id,
            )

            categoryDatabaseObjects.append(categoryDatabase)

        with self.session:
            try:
                self.session.bulk_save_objects(categoryDatabaseObjects)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to create categories for "
                             f"{categories[0].guild.name, categories[0].guild.id}", exc_info=error, )

                self.session.rollback()
            else:
                logger.debug(f"Categories created for {categories[0].guild.name, categories[0].guild.id}")

    async def _findMissingCategories(self, guild: Guild):
        """
        Check for missing categories in the guild

        :param guild: Guild to check
        :return:
        """
        categoryIdsAsTEXT = ", ".join([f"({str(category.id)})" for category in guild.categories])
        sql = text("CALL FindMissingCategories(:categoryIds, @missing_categories);")

        with self.session:
            try:
                self.session.execute(sql, {"categoryIds": categoryIdsAsTEXT})
                result = self.session.execute(text("SELECT @missing_categories;")).fetchall()

                if not result or not result[0][0]:
                    logger.debug(f"No missing categories found in guild {guild.name, guild.id}")

                    return

                categoryIDsStr = result[0][0][1:-1]
                missingCategories = list(map(int, categoryIDsStr.split(',')))
            except Exception as error:
                logger.error(f"Failed to find missing categories in guild {guild.name, guild.id}", exc_info=error)

                return

        categories = []

        for id in missingCategories:
            try:
                category = await self.client.fetch_channel(id)

                if not category:
                    logger.error(f"Category {id} not found in guild {guild.name, guild.id}")

                    continue
            except Exception as error:
                logger.error(f"Failed to fetch category {id} in guild {guild.name, guild.id}", exc_info=error)

                continue
            else:
                categories.append(category)

        await self._createCategories(categories)

    async def _findDeletedCategories(self, guild: Guild):
        """
        Check for deleted categories in the guild

        :param guild: Guild to check
        :return:
        """
        with self.session:
            try:
                selectClause = (select(Category)
                                .where(Category.guild_id == guild.id))
                guildCategories = self.session.execute(selectClause).scalars().all()

                for category in guildCategories:
                    if category.category_id not in [discordCategory.id for discordCategory in guild.categories]:
                        category.deleted_at = datetime.now()

                self.session.commit()

                logger.debug(f"Deleted categories updated for guild {guild.name, guild.id}")
            except Exception as error:
                self.session.rollback()

                logger.error(f"Failed to delete categories in guild {guild.name, guild.id}", exc_info=error)

    async def onGuildStartupCheck(self, guild: Guild):
        """
        Start up check for categories

        :param guild: Guild to check
        :return:
        """
        await self._findMissingCategories(guild)
        await self._findDeletedCategories(guild)

    async def onGuildChannelUpdate(self, before: GuildChannel, after: GuildChannel):
        """
        Update the category in the database

        :param before: Category before the update
        :param after: Category after the update
        :return:
        """
        if not before.type == discord.ChannelType.category:
            logger.debug(f"Channel {before.name, before.id} is not a category")

            return

        with self.session:
            try:
                selectQuery = (select(Category).where(Category.category_id == before.id))
                databaseCategory: Category = self.session.execute(selectQuery).scalars().one()
            except Exception as error:
                logger.error(f"Failed to fetch category {before.name, before.id}", exc_info=error)

                return

            databaseCategory.name = after.name

            try:
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to update category {before.name, before.id}", exc_info=error)

                self.session.rollback()

    def registerListener(self):
        """
        Register the listeners for the client

        :return:
        """
        self.client.addListener(self.onGuildChannelCreate, ClientListenerType.CHANNEL_CREATE)
        logger.debug("Category create listener registered")

        self.client.addListener(self.onGuildChannelDelete, ClientListenerType.CHANNEL_DELETE)
        logger.debug("Category delete listener registered")

        self.client.addListener(self.onGuildChannelUpdate, ClientListenerType.CHANNEL_UPDATE)
        logger.debug("Category update listener registered")

        self.guildManager.addListener(self.onGuildStartupCheck, GuildListenerType.START_UP)
        logger.debug("Guild manager listener registered")

        self.guildManager.addListener(self.onGuildStartupCheck, GuildListenerType.GUILD_JOIN)
        logger.debug("Guild join listener registered")

        logger.debug("Registered listeners to client")

    async def onGuildJoin(self, guild: Guild):
        pass
