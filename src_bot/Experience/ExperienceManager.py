from discord import Member

from database.Domain.models import ExperienceBoostMapping, Experience, ExperienceAmount
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Event.TimeCalculator import TimeCalculator

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src_bot.Logging.Logger import Logger

logger = Logger("ExperienceManager")


class ExperienceManager:

    def __init__(self, timeCalculator: TimeCalculator):
        self.timeCalculator = timeCalculator

        self.session = getSession()

        self.registerListener()

    def registerListener(self):
        pass

    async def calculateExperience(self, member: Member, onlineTime: int, streamTime: int, muteTime: int):
        getExperienceBoostMappingQuery = (select(ExperienceBoostMapping)
                                          .where(ExperienceBoostMapping.discord_id == member.id,
                                                 ExperienceBoostMapping.guild_id == member.guild.id, ))
        getExperienceQuery = (select(Experience).where(Experience.discord_id == member.id,
                                                       Experience.guild_id == member.guild.id, ))
        getExperienceAmountQuery = (select(ExperienceAmount))

        with self.session:
            try:
                experienceBoostMappings = self.session.execute(getExperienceBoostMappingQuery).scalars().all()
                experience = self.session.execute(getExperienceQuery).scalars().one()
                experienceAmounts = self.session.execute(getExperienceAmountQuery).scalars().all()
            except NoResultFound:
                logger.debug(f"No experience found for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}")

                experience = Experience(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                )

                self.session.add(experience)
            except Exception as error:
                logger.error(f"Failed to get experience for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}",
                             exc_info=error, )

                return

            if len(experienceAmounts) == 0:
                logger.error(f"No experience amounts found")

                return

            realOnlineTime = onlineTime - muteTime
            realStreamTime = streamTime - muteTime
            newXp = 0

            for boostMapping in experienceBoostMappings:
                # TODO dont calculate boosts if the member leaves, calculate them with history after they run out