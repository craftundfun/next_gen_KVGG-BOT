from datetime import date

from discord import Client, Member
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from database.Domain.models import Statistic
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Event.TimeCalculator import TimeCalculator
from src_bot.Logging.Logger import Logger
from src_bot.Types.TimeCalculatorType import TimeCalculatorType

logger = Logger("StatisticManager")


class StatisticManager:

    def __init__(self, client: Client, timeCalculator: TimeCalculator):
        self.client = client
        self.timeCalculator = timeCalculator
        self.session = getSession()

        self.registerListener()

    def registerListener(self):
        """
        Register the listener for the statistic manager.
        """
        self.timeCalculator.addListener(TimeCalculatorType.MEMBER_LEAVE, self.increaseStatistic)
        logger.debug("TimeCalculator listener successfully registered")

    # TODO maybe manage the increasing stats in the parameter of the function in another way
    async def increaseStatistic(self, member: Member, date: date, onlineTime: int = 0, muteTime: int = 0,
                                deafTime: int = 0, streamTime: int = 0):
        """
        Increase the statistics of the given member by the given values. If the statistic doesn't exist yet, it will be
        created.

        :param member: Member to increase the statistics for.
        :param date: Date of the statistics.
        :param onlineTime: Online time to increase.
        :param muteTime: Mute time to increase.
        :param deafTime: Deaf time to increase.
        :param streamTime: Stream time to increase.
        """
        selectQuery = (select(Statistic)
                       .where(Statistic.discord_id == member.id,
                              Statistic.guild_id == member.guild.id,
                              Statistic.date == date, ))

        with self.session:
            try:
                statistic = self.session.execute(selectQuery).scalars().one()
            except NoResultFound:
                statistic = Statistic(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    date=date,
                    online_time=0,
                    mute_time=0,
                    deaf_time=0,
                    stream_time=0,
                    message_count=0,
                    command_count=0,
                )

                self.session.add(statistic)
            except Exception as error:
                logger.error(
                    f"Couldn't fetch or create statistic for {member.display_name, member.id} on "
                    f"{member.guild.name, member.guild.id} at the date {date}",
                    exc_info=error,
                )

                self.session.rollback()

                return

            statistic.online_time += onlineTime
            statistic.mute_time += muteTime
            statistic.deaf_time += deafTime
            statistic.stream_time += streamTime

            try:
                self.session.commit()
            except Exception as error:
                logger.error(
                    f"Couldn't commit changes for {member.display_name, member.id} on "
                    f"{member.guild.name, member.guild.id} at the date {date}",
                    exc_info=error,
                )

                self.session.rollback()

                return
            else:
                logger.debug(
                    f"Updated statistics for {member.display_name, member.id} on "
                    f"{member.guild.name, member.guild.id} at the date {date}",
                )

                return
