from datetime import datetime

from discord import Member, User
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.DiscordUser.Entity.DiscordUser import DiscordUser
from database.Domain.Guild.Entity.Guild import Guild
from database.Domain.Guild.Entity.GuildDiscordUserMapping import GuildDiscordUserMapping
from src.Client.Client import Client
from src.Database.DatabaseConnection import getSession
from src.Logging.Logger import Logger
from src.Types.ClientListenerType import ClientListenerType

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

        self.client.addListener(self.memberLeftGuild, ClientListenerType.MEMBER_REMOVE)
        logger.debug("Registered member remove listener")

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
            except Exception as error:
                logger.error(f"Failed to get member {member.name, member.id}", exc_info=error)

                return
            else:
                logger.debug(f"Member {member.name, member.id} found in database")

            # Get the guild from the database
            try:
                selectQuery = (select(Guild).where(Guild.guild_id == member.guild.id))
                databaseGuild = self.session.execute(selectQuery).scalars().one()
            except Exception as error:
                logger.error(f"Failed to get guild {member.guild.name, member.guild.id}", exc_info=error)

                return
            else:
                logger.debug(f"Guild {member.guild.name, member.guild.id} found in database")

            # Add the member to the guild
            try:
                guildDiscordUserMapping = GuildDiscordUserMapping(
                    guild_id=databaseGuild.guild_id,
                    discord_user_id=databaseMember.discord_id,
                    display_name=member.display_name,
                )

                self.session.add(guildDiscordUserMapping)
                self.session.commit()
            except Exception as error:
                logger.error(f"Failed to add member {member.name, member.id} to guild "
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

    async def memberLeftGuildRaw(self, guildId: int, user: User):
        """
        Remove a member from the guild using the user object because the member object is not available

        :param guildId: Guild ID
        :param user: User object
        :return:
        """
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
