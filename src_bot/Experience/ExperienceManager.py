from datetime import timedelta, datetime

from discord import Guild, Member
from sqlalchemy import select

from database.Domain.models import ExperienceBoostMapping
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Guild.GuildManager import GuildManager
from src_bot.Logging.Logger import Logger
from src_bot.Timer.Timer import Timer
from src_bot.Types.GuildListenerType import GuildListenerType

logger = Logger("ExperienceManager")


class ExperienceManager:

    def __init__(self, client: Client, timer: Timer, guildManager: GuildManager):
        self.client = client
        self.timer = timer
        self.guildManager = guildManager

        self.session = getSession()

        self.registerListener()

    def registerListener(self):
        self.guildManager.addGuildManagerListener(self.startTimers, GuildListenerType.START_UP)
        logger.debug("Registered guild manager listener")

    async def startTimers(self, guild: Guild):
        """
        Start the timers for the experience boosts for members that are online

        :param guild: Guild to start the timers for
        """
        with self.session:
            for member in guild.members:
                if not member.voice:
                    continue

                logger.debug(f"{member.display_name, member.id} is in voice-channel")

                selectQuery = (select(ExperienceBoostMapping)
                               .where(ExperienceBoostMapping.guild_id == guild.id,
                                      ExperienceBoostMapping.discord_id == member.id, ))

                try:
                    boostMappings = self.session.execute(selectQuery).scalars().fetchall()
                except Exception as error:
                    logger.error(
                        f"Failed to get boost mappings for {member.display_name, member.id} on "
                        f"{guild.name, guild.id}",
                        exc_info=error,
                    )

                    continue

                if not boostMappings or len(boostMappings) == 0:
                    logger.debug(
                        f"No boost mappings found for {member.display_name, member.id} on "
                        f"{guild.name, guild.id}"
                    )

                    continue

                for boostMapping in boostMappings:
                    self.timer.addJob(
                        self.boostEnded,
                        datetime.now() + timedelta(seconds=boostMapping.remaining_time),
                        f"experience-{guild.id}-{member.id}",
                        member=member,
                        guild=guild,
                    )

                    logger.debug(
                        f"Added job for {boostMapping} for {member.display_name, member.id} on "
                        f"{guild.name, guild.id}"
                    )

                logger.debug(f"Added jobs for {member.display_name, member.id} on {guild.name, guild.id}")

    async def boostEnded(self, member: Member, guild: Guild):
        print(f"{datetime.now()} Hello {member} on {guild}")
