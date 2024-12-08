from datetime import timedelta

from database.Domain.models import History, Statistic
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Event.EventHandler import EventHandler
from src_bot.Logging.Logger import Logger
from src_bot.Types.EventHandlerType import EventHandlerType
from discord import Member
from sqlalchemy import select, update
from sqlalchemy.orm.exc import NoResultFound

logger = Logger("TimeCalculator")


class TimeCalculator:

    def __init__(self, eventHandler: EventHandler):
        self.eventHandler = eventHandler
        self.session = getSession()

        self.registerListener()

    def registerListener(self):
        self.eventHandler.addListener(EventHandlerType.MEMBER_LEAVE, self.onMemberLeave)

    async def onMemberLeave(self, member: Member):
        # select all events that did happen since the last time the member joined
        selectQuery = (
            select(History)
            .where(
                History.discord_id == member.id,
                History.guild_id == member.guild.id,
                History.time >= (
                    select(History.time)
                    .where(
                        History.discord_id == member.id,
                        History.guild_id == member.guild.id,
                        History.event_id == 7,
                    )
                    .order_by(History.time.desc())
                    .limit(1)
                    .scalar_subquery()
                ),
            )
            .order_by(History.time.desc())
        )

        with self.session:
            try:
                result = self.session.execute(selectQuery).scalars().all()
            except Exception as error:
                logger.error("Error while executing select query", exc_info=error)

            onlineTime: timedelta = result[0].time - result[-1].time
            logger.debug(f"Raw online time for {member.display_name, member.id} on "
                         f"{member.guild.name, member.guild.id}: {onlineTime}")

            muteEvents = []
            unmuteEvents = []
            for index, history in enumerate(result, 0):
                if history.event_id == 1:
                    muteEvents.append(history)
                elif history.event_id == 2:
                    unmuteEvents.append(history)

            if len(muteEvents) == len(unmuteEvents):
                for i in range(len(muteEvents)):
                    onlineTime -= unmuteEvents[i].time - muteEvents[i].time

                logger.debug(f"Mute and unmute events match for {member.display_name, member.id} "
                             f"on {member.guild.name, member.guild.id}")
            else:
                logger.error(f"Mute and unmute events do not match for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}, trying to recover.")

                stack = []
                for muteEvent in muteEvents:
                    stack.append(muteEvent)

                    for unmuteEvent in unmuteEvents:
                        if stack[-1].time < unmuteEvent.time:
                            onlineTime -= unmuteEvent.time - stack[-1].time
                            stack.pop()
                            break

                logger.debug(f"Recovered online time for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}: {onlineTime}")

            logger.debug(f"Online time for {member.display_name, member.id} on "
                         f"{member.guild.name, member.guild.id}: {onlineTime}")

            selectQuery = (select(Statistic)
                           .where(Statistic.discord_id == member.id,
                                  Statistic.guild_id == member.guild.id))

            # get the statistic for the member and simultaneously check if they already have one
            try:
                statistic = self.session.execute(selectQuery).scalars().one()
            except NoResultFound:
                statistic = Statistic(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    # it has a default yes, but until its committed the object does not have it and its None
                    online_time=0,
                )

                logger.debug(f"Created new statistic for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}")
            except Exception as error:
                logger.error("Error while updating online time", exc_info=error)
                self.session.rollback()

                return

            statistic.online_time += int(onlineTime.total_seconds())

            try:
                self.session.add(statistic)
                self.session.commit()
            except Exception as error:
                logger.error("Error while committing changes", exc_info=error)
                self.session.rollback()
            else:
                logger.debug(f"Updated online time for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}")
