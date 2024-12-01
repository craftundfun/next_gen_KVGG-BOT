from datetime import datetime

from discord import Member, User, RawMemberRemoveEvent
from sqlalchemy import select, null
from sqlalchemy.exc import NoResultFound

from Bot.database.Domain.DiscordUser.Entity.DiscordUser import DiscordUser
from Bot.database.Domain.Guild.Entity.GuildDiscordUserMapping import GuildDiscordUserMapping
from Bot.src.Client.Client import Client
from Bot.src.Database.DatabaseConnection import getSession
from Bot.src.Logging.Logger import Logger
from Bot.src.Types.ClientListenerType import ClientListenerType

logger = Logger("MemberManager")


class MemberManager:

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()

        self.registerListener()

    def registerListener(self):
        """
        Register all necessary listeners

        :return:
        """
        self.client.addListener(self.memberJoinGuild, ClientListenerType.MEMBER_JOIN)
        logger.debug("Registered member join listener")

        """the raw event is called everytime, use that to avoid unnecessary database calls"""
        # self.client.addListener(self.memberLeftGuild, ClientListenerType.MEMBER_REMOVE)
        # logger.debug("Registered member remove listener")

        self.client.addListener(self.memberLeftGuildRaw, ClientListenerType.RAW_MEMBER_REMOVE)
        logger.debug("Registered raw member remove listener")

        self.client.addListener(self.memberUpdate, ClientListenerType.MEMBER_UPDATE)
        logger.debug("Registered member update listener")

    async def memberJoinGuild(self, member: Member):
        """
        Adds a member to the database when they join a guild

        :param member: Member that joined the guild. Member is specific to the guild.
        :return:
        """
        with self.session:
            # Get the member from the database
            try:
                selectQuery = (select(DiscordUser).where(DiscordUser.discord_id == member.id))
                databaseMember = self.session.execute(selectQuery).scalars().one()
            except NoResultFound:
                databaseMember = DiscordUser(
                    discord_id=member.id,
                    global_name=member.name,
                    created_at=member.created_at,
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
                                      GuildDiscordUserMapping.discord_user_id == member.id, ))
                guildDiscordUserMapping = self.session.execute(selectQuery).scalars().one()
            except NoResultFound:
                try:
                    guildDiscordUserMapping = GuildDiscordUserMapping(
                        guild_id=member.guild.id,
                        discord_user_id=databaseMember.discord_id,
                        display_name=member.display_name,
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
                guildDiscordUserMapping.left_at = null()

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

    async def memberLeftGuild(self, member: Member):
        """
        Remove a member from the guild

        :param member: Guild specific member that left the guild
        :return:
        """
        with self.session:
            try:
                selectQuery = (select(GuildDiscordUserMapping)
                               .where(GuildDiscordUserMapping.guild_id == member.guild.id,
                                      GuildDiscordUserMapping.discord_user_id == member.id))
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

    async def memberLeftGuildRaw(self, payload: RawMemberRemoveEvent):
        """
        Remove a member from the guild using the user object because the member object is not available

        :param payload: Raw member remove event
        :return:
        """
        guildId: int = payload.guild_id
        user: User = payload.user

        with self.session:
            try:
                selectQuery = (select(GuildDiscordUserMapping)
                               .where(GuildDiscordUserMapping.guild_id == guildId,
                                      GuildDiscordUserMapping.discord_user_id == user.id))
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

    async def memberUpdate(self, before: Member, after: Member):
        # TODO

        pass
