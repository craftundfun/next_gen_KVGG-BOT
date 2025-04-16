from datetime import datetime

from discord import Member, User, RawMemberRemoveEvent, Guild
from sqlalchemy import select, null
from sqlalchemy.exc import NoResultFound

from database.Domain.models.DiscordUser import DiscordUser
from database.Domain.models.GuildDiscordUserMapping import GuildDiscordUserMapping
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Guild.GuildManager import GuildManager
from src_bot.Interface.Client.ClientMemberListenerInterface import ClientMemberListenerInterface
from src_bot.Interface.Guild.GuildListenerInterface import GuildListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType
from src_bot.Types.GuildListenerType import GuildListenerType

logger = Logger("MemberManager")


class MemberManager(ClientMemberListenerInterface, GuildListenerInterface):

    def __init__(self, client: Client, guildManager: GuildManager):
        self.client = client
        self.guildManager = guildManager

        self.session = getSession()

        self.registerListener()

    def registerListener(self):
        """
        Register all necessary listeners

        :return:
        """
        self.client.addListener(self.onMemberJoin, ClientListenerType.MEMBER_JOIN)
        logger.debug("Registered member join listener")

        """the raw event is called everytime, use that to avoid unnecessary database calls"""
        # self.client.addListener(self.memberLeftGuild, ClientListenerType.MEMBER_REMOVE)
        # logger.debug("Registered member remove listener")

        self.client.addListener(self.onRawMemberRemove, ClientListenerType.RAW_MEMBER_REMOVE)
        logger.debug("Registered raw member remove listener")

        self.client.addListener(self.onMemberUpdate, ClientListenerType.MEMBER_UPDATE)
        logger.debug("Registered member update listener")

        self.guildManager.addListener(self.onGuildStartupCheck, GuildListenerType.START_UP)
        logger.debug("Registered guild manager start up listener")

    # TODO detect members that left the guild while the bot was offline
    async def onGuildStartupCheck(self, guild: Guild):
        """
        Add all (missing) members of a guild to the database when the bot starts

        :param guild: Guild to add members to the database
        """
        with self.session:
            selectQueryForGuildSpecific = (select(DiscordUser)
                                           .join(GuildDiscordUserMapping)
                                           .where(GuildDiscordUserMapping.guild_id == guild.id))
            selectQueryForAllDiscordUsers = select(DiscordUser)

            try:
                discordUsers = self.session.execute(selectQueryForAllDiscordUsers).scalars().all()
            except Exception as error:
                logger.error("Failed to get all members from database", exc_info=error)

                return

            try:
                discordUsersForGuild = self.session.execute(selectQueryForGuildSpecific).scalars().all()
            except NoResultFound:
                logger.debug(f"No members in database for guild {guild.name, guild.id}")

                membersToAdd = list(guild.members)
            except Exception as error:
                logger.error(f"Failed to get all members from database for guild {guild.name, guild.id}",
                             exc_info=error)

                return
            else:
                discordUserIds: list[int] = [discordUser.discord_id for discordUser in discordUsersForGuild]
                membersToAdd: list[Member] = [member for member in guild.members
                                              if member.id not in discordUserIds]

            if not membersToAdd:
                logger.debug(f"No members to add to database for guild {guild.name, guild.id}")

                return

            newDiscordUsers: list[DiscordUser] = []
            newGuildMappings: list[GuildDiscordUserMapping] = []

            for member in membersToAdd:
                if member.bot:
                    logger.debug(f"Discord {member.display_name, member.id} is a bot on guild {guild.name, guild.id}")

                    continue

                newDiscordUserInserted = False
                newGuildMappingInserted = False

                try:
                    # the corresponding DiscordUser may already exist in the database
                    if member.id not in [discordUser.discord_id for discordUser in discordUsers]:
                        newDiscordUsers.append(
                            DiscordUser(
                                discord_id=member.id,
                                global_name=member.name,
                            )
                        )

                        newDiscordUserInserted = True

                    newGuildMappings.append(
                        GuildDiscordUserMapping(
                            guild_id=guild.id,
                            discord_id=member.id,
                            display_name=member.display_name,
                            # TODO better profile picture handling => guild specific, global, etc.
                            profile_picture=member.display_avatar.url if member.display_avatar else None,
                            joined_at=member.joined_at if member.joined_at else datetime.now(),
                        )
                    )

                    newGuildMappingInserted = True
                except Exception as error:
                    logger.error(f"Couldn't add DiscordUser for member {member.name, member.id} "
                                 f"or GuildMapping for guild {guild.name, guild.id}",
                                 exc_info=error, )

                    # dont insert half of the data
                    if newDiscordUserInserted:
                        newDiscordUsers.pop()

                    if newGuildMappingInserted:
                        newGuildMappings.pop()

                    continue

            try:
                self.session.bulk_save_objects(newDiscordUsers)
                self.session.bulk_save_objects(newGuildMappings)
                self.session.commit()
            except Exception as error:
                logger.error("Couldn't bulk add DiscordUsers and GuildMappings", exc_info=error)

                self.session.rollback()

                return

            logger.debug(f"Added new DiscordUsers and GuildMappings to the database for guild {guild.name, guild.id}")

    async def onMemberJoin(self, member: Member):
        """
        Adds a member to the database when they join a guild

        :param member: Member that joined the guild. Member is specific to the guild.
        :return:
        """
        with self.session:
            # Get the member from the database
            try:
                selectQuery = (select(DiscordUser).where(DiscordUser.discord_id == member.id, ))
                databaseMember = self.session.execute(selectQuery).scalars().one()
            except NoResultFound:
                databaseMember = DiscordUser(
                    discord_id=member.id,
                    global_name=member.name,
                )

                self.session.add(databaseMember)
                logger.debug(f"Member {member.name, member.id} added to database")
            except Exception as error:
                self.session.rollback()
                logger.error(f"Failed to get member {member.name, member.id}", exc_info=error)

                return
            else:
                logger.debug(f"Member {member.name, member.id} found in database")

            # Fetch old guild member mapping or create a new one
            try:
                selectQuery = (select(GuildDiscordUserMapping)
                               .where(GuildDiscordUserMapping.guild_id == member.guild.id,
                                      GuildDiscordUserMapping.discord_id == member.id, ))
                guildDiscordUserMapping = self.session.execute(selectQuery).scalars().one()
            except NoResultFound:
                try:
                    guildDiscordUserMapping = GuildDiscordUserMapping(
                        guild_id=member.guild.id,
                        discord_id=databaseMember.discord_id,
                        display_name=member.display_name,
                        profile_picture=member.display_avatar.url if member.display_avatar else None,
                        joined_at=member.joined_at if member.joined_at else datetime.now(),
                    )

                    self.session.add(guildDiscordUserMapping)
                    logger.debug(f"Member {member.name, member.id} added to guild {member.guild.name, member.guild.id}")
                except Exception as error:
                    logger.error(f"Failed to add member {member.name, member.id} to guild "
                                 f"{member.guild.name, member.guild.id}",
                                 exc_info=error, )
                    self.session.rollback()

                    return
            except Exception as error:
                logger.error(f"Failed to get guild member mapping for {member.name, member.id} "
                             f"and {member.guild.name, member.guild.id}",
                             exc_info=error, )

                return
            else:
                # set left_at to null if the member rejoined the guild
                guildDiscordUserMapping.left_at = null()
                # update joined_at to the current time
                guildDiscordUserMapping.joined_at = member.joined_at if member.joined_at else datetime.now()

            try:
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to add or edit member {member.name, member.id} for guild "
                             f"{member.guild.name, member.guild.id}",
                             exc_info=error, )
                self.session.rollback()

                return
            else:
                logger.debug(f"Member {member.name, member.id} added to guild {member.guild.name, member.guild.id}")

    async def onMemberRemove(self, member: Member):
        """
        Remove a member from the guild

        :param member: Guild specific member that left the guild
        :return:
        """
        with self.session:
            try:
                selectQuery = (select(GuildDiscordUserMapping)
                               .where(GuildDiscordUserMapping.guild_id == member.guild.id,
                                      GuildDiscordUserMapping.discord_id == member.id))
                guildDiscordUserMapping = self.session.execute(selectQuery).scalars().one()
                guildDiscordUserMapping.left_at = datetime.now()

                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to get guild member mapping {member.name, member.id} "
                             f"for guild {member.guild.name, member.guild.id}", exc_info=error)

                self.session.rollback()
                return
            else:
                logger.debug(f"Member {member.name, member.id} removed from guild {member.guild.name, member.guild.id}")

    async def onRawMemberRemove(self, payload: RawMemberRemoveEvent):
        """
        Remove a member from the guild using the user object because the member object is not available

        :param payload: Raw member remove event
        :return:
        """
        guildId: int = payload.guild_id
        user: User = payload.user

        with self.session:
            try:
                selectQuery = (
                    select(GuildDiscordUserMapping)
                    .where(
                        GuildDiscordUserMapping.guild_id == guildId,
                        GuildDiscordUserMapping.discord_id == user.id,
                    )
                )
                guildDiscordUserMapping = self.session.execute(selectQuery).scalars().one()
                guildDiscordUserMapping.left_at = datetime.now()

                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to get guild member mapping {user.name, user.id} "
                             f"for guild {guildId}", exc_info=error)

                self.session.rollback()
                return
            else:
                logger.debug(f"Member {user.name, user.id} removed from guild {guildId}")

    async def onMemberUpdate(self, before: Member, after: Member):
        # TODO

        pass

    async def onGuildJoin(self, guild: Guild):
        pass
