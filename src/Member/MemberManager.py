from discord import Member
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
        self.client.addListener(self.memberJoinGuild, ClientListenerType.MEMBER_JOIN)
        logger.debug("Registered member join listener")

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
