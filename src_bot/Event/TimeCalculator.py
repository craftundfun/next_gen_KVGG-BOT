from datetime import timedelta
from typing import Sequence

from discord import Member
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from database.Domain.models import History, Statistic
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Event.EventHandler import EventHandler
from src_bot.Logging.Logger import Logger
from src_bot.Types.EventHandlerType import EventHandlerType

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
            .order_by(History.time.asc())
        )

        with self.session:
            try:
                history = self.session.execute(selectQuery).scalars().all()
            except Exception as error:
                logger.error("Error while executing select query", exc_info=error)

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
                    mute_time=0,
                    deaf_time=0,
                    stream_time=0,
                )

                logger.debug(f"Created new statistic for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}")
            except Exception as error:
                logger.error("Error while updating online time", exc_info=error)
                self.session.rollback()

                return

            onlineTime, muteTime = self._calculateOnlineTime(member, history)
            statistic.online_time += onlineTime
            statistic.mute_time += muteTime

            statistic.stream_time += self._calculateStreamTime(member, history)

            try:
                # add regardless of whether the member has a statistic or not
                self.session.add(statistic)
                self.session.commit()
            except Exception as error:
                logger.error("Error while committing changes", exc_info=error)
                self.session.rollback()
            else:
                logger.debug(f"Updated online time for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}")

    def _calculateOnlineTime(self, member: Member, history: Sequence[History]) -> (int, int):
        """
        Calculate the online time of a member by subtracting the time they were muted from the time they were online.

        :param member: The member to calculate the online time for.
        :param history: The history of the member.
        """
        onlineTime: timedelta = history[-1].time - history[0].time
        logger.debug(f"Raw online time for {member.display_name, member.id} on "
                     f"{member.guild.name, member.guild.id}: {onlineTime}")

        muteTime = timedelta()

        muteEvents = []
        unmuteEvents = []

        for history in history:
            if history.event_id == 1:
                muteEvents.append(history)
            elif history.event_id == 2:
                unmuteEvents.append(history)

        if len(muteEvents) == len(unmuteEvents):
            for i in range(len(muteEvents)):
                muteTime += unmuteEvents[i].time - muteEvents[i].time

            logger.debug(f"Mute and unmute events match for {member.display_name, member.id} "
                         f"on {member.guild.name, member.guild.id}")
        else:
            # maybe use a lower log level here in the future
            logger.error(f"Mute and unmute events do not match for {member.display_name, member.id} on "
                         f"{member.guild.name, member.guild.id}, trying to recover.")

            # use a try block here in case anything goes wrong
            try:
                # more mutes than unmutes
                if len(muteEvents) > len(unmuteEvents):
                    for i in range(len(muteEvents) - 1):
                        for j in range(len(unmuteEvents)):
                            # if the unmute event is between two mute events
                            if muteEvents[i].time <= unmuteEvents[j].time <= muteEvents[i + 1].time:
                                muteTime += unmuteEvents[j].time - muteEvents[i].time

                                break

                    if len(unmuteEvents) > 0:
                        # if the last unmute event is after the last mute event
                        if unmuteEvents[-1].time >= muteEvents[-1].time:
                            muteTime += unmuteEvents[-1].time - muteEvents[-1].time
                else:
                    usedMuteIndex = []

                    for i in range(len(unmuteEvents)):
                        for j in range(len(muteEvents)):
                            # if the mute event is before the unmute event, and it has not been used yet
                            if muteEvents[j].time <= unmuteEvents[i].time and not j in usedMuteIndex:
                                muteTime += unmuteEvents[i].time - muteEvents[j].time
                                usedMuteIndex.append(j)

                                break
            except Exception as error:
                logger.error("Error while trying to recover online time", exc_info=error)

        logger.debug(f"Online time for {member.display_name, member.id} on "
                     f"{member.guild.name, member.guild.id}: {onlineTime}")

        return int(onlineTime.total_seconds()), int(muteTime.total_seconds())

    def _calculateStreamTime(self, member: Member, history: Sequence[History]) -> int:
        streamStartEvents = []
        streamStopEvents = []

        for history in history:
            if history.event_id == 5:
                streamStartEvents.append(history)
            elif history.event_id == 6:
                streamStopEvents.append(history)

        # if one of the lists is empty, the member did not stream or we cant recover the time
        if len(streamStartEvents) == 0 or len(streamStopEvents) == 0:
            logger.debug(f"{member.display_name, member.id} on {member.guild.name, member.guild.id} did not stream or "
                         f"we are unable to recover the time, idk tho")

            return 0

        streamTime = timedelta()

        if len(streamStartEvents) == len(streamStopEvents):
            logger.debug(f"Stream start and stop events match for {member.display_name, member.id} on "
                         f"{member.guild.name, member.guild.id}")

            for i in range(len(streamStartEvents)):
                streamTime += streamStopEvents[i].time - streamStartEvents[i].time

            logger.debug(f"Stream time for {member.display_name, member.id} on {member.guild.name, member.guild.id}: "
                         f"{streamTime}")

            return int(streamTime.total_seconds())
        else:
            logger.error(f"Stream start and stop events do not match for {member.display_name, member.id} on "
                         f"{member.guild.name, member.guild.id}, trying to recover.")

            try:
                # more start events than stop events
                if len(streamStartEvents) > len(streamStopEvents):
                    for i in range(len(streamStartEvents) - 1):
                        for j in range(len(streamStopEvents)):
                            # if the stop event is between two start events
                            if streamStartEvents[i].time <= streamStopEvents[j].time <= streamStartEvents[i + 1].time:
                                streamTime += streamStopEvents[j].time - streamStartEvents[i].time

                                break

                    if len(streamStopEvents) > 0:
                        # if the last stop event is after the last start event
                        if streamStopEvents[-1].time >= streamStartEvents[-1].time:
                            streamTime += streamStopEvents[-1].time - streamStartEvents[-1].time
                else:
                    usedStartIndex = []

                    for i in range(len(streamStopEvents)):
                        for j in range(len(streamStartEvents)):
                            # if the start event is before the stop event, and it has not been used yet
                            if streamStartEvents[j].time <= streamStopEvents[i].time and not j in usedStartIndex:
                                streamTime += streamStopEvents[i].time - streamStartEvents[j].time
                                usedStartIndex.append(j)

                                break

                logger.debug(f"Recovered stream time for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}: {streamTime}")

                return int(streamTime.total_seconds())
            except Exception as error:
                logger.error("Error while trying to recover stream time", exc_info=error)

                return int(streamTime.total_seconds())
