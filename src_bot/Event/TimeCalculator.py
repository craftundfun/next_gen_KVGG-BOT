from datetime import timedelta, datetime
from typing import Sequence

from discord import Member
from sqlalchemy import select, null
from sqlalchemy.orm.exc import NoResultFound

from database.Domain.models import History, Statistic
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Event.EventHandler import EventHandler
from src_bot.Helpers.FunctionName import listenerName
from src_bot.Logging.Logger import Logger
from src_bot.Types.EventHandlerType import EventHandlerType
from src_bot.Types.TimeCalculatorType import TimeCalculatorType

logger = Logger("TimeCalculator")


class TimeCalculator:
    memberLeaveListeners = []

    def __init__(self, eventHandler: EventHandler):
        self.eventHandler = eventHandler
        self.session = getSession()

        self.registerListener()

    def addListener(self, type: TimeCalculatorType, listener: callable):
        """
        Add a listener to the time calculator.

        :param type: The type of the listener.
        :param listener: The listener to add.
        """
        match type:
            case TimeCalculatorType.MEMBER_LEAVE:
                self.memberLeaveListeners.append(listener)
            case _:
                logger.error(f"Unknown time calculator type {type}")

                return

        logger.debug(f"Listener successfully added: {listenerName(listener)}")

    def registerListener(self):
        """
        Register the listener for the time calculator.
        """
        self.eventHandler.addListener(EventHandlerType.MEMBER_LEAVE, self.onMemberLeave)

    async def onMemberLeave(self, member: Member):
        """
        Fetch the online history and invoke the online and stream time calculation.

        :param member: The member that left the channel.
        """
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

                return

            editedHistory = self._insertMidnightEvent(history, member)

            # TODO remove after debugging
            if type(editedHistory) is dict:
                for key in editedHistory.keys():
                    print(key, editedHistory[key])

            selectQuery = (select(Statistic)
                           .where(Statistic.discord_id == member.id,
                                  Statistic.guild_id == member.guild.id, ))

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
                logger.error(f"Error while fetching statistic for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}", exc_info=error)
                self.session.rollback()

                return

            onlineTimes = {}
            streamTimes = {}

            if type(editedHistory) is list:
                onlineTime, muteTime = self._calculateOnlineTime(member, history)
                onlineTimes[datetime.now().date()] = (onlineTime, muteTime,)

                streamTime = self._calculateStreamTime(member, history)
                streamTimes[datetime.now().date()] = streamTime
            else:
                for date in editedHistory.keys():
                    onlineTime, muteTime = self._calculateOnlineTime(member, editedHistory[date])
                    onlineTimes[date] = (onlineTime, muteTime,)

                    streamTime = self._calculateStreamTime(member, editedHistory[date])
                    streamTimes[date] = streamTime

            try:
                # add regardless of whether the member has a statistic or not
                self.session.add(statistic)
                self.session.commit()
            except Exception as error:
                logger.error("Error while committing changes", exc_info=error)
                self.session.rollback()

                return
            else:
                logger.debug(f"Updated statistics for {member.display_name, member.id} on "
                             f"{member.guild.name, member.guild.id}")

        for listener in self.memberLeaveListeners:
            await listener(member, onlineTime, streamTime, muteTime)
            logger.debug(f"Invoked listener: {listenerName(listener)}")

    def _insertMidnightEvent(self, historyFromMember: Sequence[History], member: Member) \
            -> dict[datetime.date, list[History]] | Sequence[History]:
        """
        If the user was online over midnight, leave events are inserted at midnight and join events after midnight
        to have one leave-join circle per day.
        This makes it easier to calculate the time.

        :param historyFromMember: The history of the member.
        :param member: Just for logging purposes.
        """
        if len(historyFromMember) == 0:
            logger.error(f"No history found for {member.display_name, member.id} on "
                         f"{member.guild.name, member.guild.id}, this should not happen")

            return historyFromMember

        # all events happened on the same day, no need to insert anything
        if historyFromMember[0].time.date() == historyFromMember[-1].time.date():
            logger.debug(f"{member.display_name, member.id} on {member.guild.name, member.guild.id} was online only on "
                         f"{datetime.now().date()}")

            return historyFromMember

        # count how many midnight events are needed
        midnightEvents = (historyFromMember[-1].time.date() - historyFromMember[0].time.date()).days
        # list of tuples with the day before and after midnight
        dates = []

        logger.debug(f"{member.display_name, member.id} on {member.guild.name, member.guild.id} was online over "
                     f"{midnightEvents} days")

        for i in range(midnightEvents):
            dates.append(historyFromMember[0].time.date() + timedelta(days=i))

        # append the current date for easier iteration
        dates.append(historyFromMember[-1].time.date())

        # save the time of the last events
        # the key is the event id
        lastEvents: dict[int, None | History] = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
        }
        dateIndex = 0
        # empty list for each day the member was online in this session
        historiesPerDay: dict[datetime.date, list[History]] = {date: [] for date in dates}

        def _getHistory(takeDataFrom: History, eventId: int = None, time: datetime = None) -> History:
            """
            Returns a new history object with the same data as the history object passed to the function.
            """
            return History(
                discord_id=takeDataFrom.discord_id,
                guild_id=takeDataFrom.guild_id,
                event_id=eventId if eventId else takeDataFrom.event_id,
                time=time if time else takeDataFrom.time,
                channel_id=takeDataFrom.channel_id,
                additional_info=takeDataFrom.additional_info if takeDataFrom.additional_info else null(),
            )

        def _getEventsForCurrentDateIndex() -> tuple[list[History], History]:
            """
            Inserts all necessary events for the current (global) date index.
            Returns the list of histories for this day and the join history for the next day.
            """
            historiesForThisDay = []
            closingEvents = []
            openingEvents = []

            beforeMidnight = datetime(
                dates[dateIndex].year,
                dates[dateIndex].month,
                dates[dateIndex].day,
                23,
                59,
                59,
                # 999 milliseconds, but the type here is microseconds
                999_000,
            )
            afterMidnight = datetime(
                dates[dateIndex + 1].year,
                dates[dateIndex + 1].month,
                dates[dateIndex + 1].day,
                0,
                0,
                0,
                0,
            )

            # look for opening events and insert a closing event
            for key in range(1, len(lastEvents)):
                # not an opening event
                if key not in [1, 3, 5]:
                    continue

                # no opening event exists
                if not (currentEvent := lastEvents[key]):
                    continue

                # when a closing event exists, check if the opening event is before the closing event
                if lastEvents[key + 1]:
                    if lastEvents[key + 1].time > currentEvent.time:
                        continue

                # close the event
                closingEvents.append(
                    _getHistory(currentEvent, eventId=currentEvent.event_id + 1, time=beforeMidnight)
                )
                # reopen the event
                openingEvents.append(
                    _getHistory(currentEvent, eventId=currentEvent.event_id, time=afterMidnight)
                )

            # close all events first
            historiesForThisDay.extend(closingEvents)
            # after that insert the leave event
            # history is coming from the for loop under this function (outer scope)
            historiesForThisDay.append(
                _getHistory(history, eventId=8, time=beforeMidnight)
            )

            # insert the join event first
            historiesForThisDay.append(
                _getHistory(history, eventId=7, time=afterMidnight)
            )
            # after that reopen all events
            historiesForThisDay.extend(openingEvents)

            return historiesForThisDay[:-1], historiesForThisDay[-1]

        # walk through the whole history once
        for history in historyFromMember:
            # when the date does not change, just add the history to the temp list
            if history.time.date() == dates[dateIndex]:
                historiesPerDay[dates[dateIndex]].append(history)

                # save the event if it is an important event
                if history.event_id in lastEvents.keys():
                    lastEvents[history.event_id] = history
            # when the date changes and there are no events between the two dates
            elif dateIndex + 1 < len(dates) and history.time.date() > dates[dateIndex + 1]:
                # one list for each day
                days = {date: [] for date in dates}

                # for each day get the correct history
                for i in range((history.time.date() - dates[dateIndex]).days):
                    historiesForThisDay, historyForNextDay = _getEventsForCurrentDateIndex()

                    # save the histories for this day
                    days[dates[dateIndex]].extend(historiesForThisDay)
                    days[dates[dateIndex + 1]].append(historyForNextDay)

                    historiesPerDay[dates[dateIndex]].extend(historiesForThisDay)
                    historiesPerDay[dates[dateIndex + 1]].append(historyForNextDay)
                    dateIndex += 1

                historiesPerDay[dates[dateIndex]].append(history)

                # unpack all events for this the days
                allDays = [event for key in days for event in days[key]]

                try:
                    # it is important to preserve the order of the events
                    self.session.bulk_save_objects(allDays, preserve_order=True)
                    self.session.commit()
                except Exception as error:
                    logger.error("Error while committing changes", exc_info=error)
                    self.session.rollback()

                    # TODO evaluate if we should really return
                    return historyFromMember
            # date changed and the next history event is on the next day
            else:
                historiesForThisDay, historyForNextDay = _getEventsForCurrentDateIndex()

                historiesPerDay[dates[dateIndex + 1]].append(historyForNextDay)
                historiesPerDay[dates[dateIndex]].extend(historiesForThisDay)

                historiesForThisDay.append(historyForNextDay)
                dateIndex += 1

                try:
                    self.session.bulk_save_objects(historiesForThisDay, preserve_order=True)
                    self.session.commit()
                except Exception as error:
                    logger.error("Error while committing changes", exc_info=error)
                    self.session.rollback()
                else:
                    logger.debug(f"Inserted midnight events for {member.display_name, member.id} "
                                 f"on {member.guild.name, member.guild.id}")

        return historiesPerDay

    def _calculateOnlineTime(self, member: Member, history: Sequence[History]) -> tuple[int, int]:
        """
        Calculate the online time of a member by subtracting the time they were muted from the time they were online.

        :param member: The member to calculate the online time for.
        :param history: The history of the member.
        :return: The online time and the mute time of the member in seconds.
        """
        onlineTime: timedelta = history[-1].time - history[0].time
        logger.debug(f"Raw online time for {member.display_name, member.id} on "
                     f"{member.guild.name, member.guild.id}: {onlineTime}")

        muteTime = timedelta()
        muteEvents = []
        unmuteEvents = []

        # find all wanted events
        for history in history:
            if history.event_id == 1:
                muteEvents.append(history)
            elif history.event_id == 2:
                unmuteEvents.append(history)

        # if
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
                logger.error(f"Error while trying to recover mute and unmute times for "
                             f"{member.display_name, member.id} on {member.guild.name, member.guild.id}",
                             exc_info=error, )

        logger.debug(f"Online time for {member.display_name, member.id} on "
                     f"{member.guild.name, member.guild.id}: {onlineTime}")

        return int(onlineTime.total_seconds()), int(muteTime.total_seconds())

    def _calculateStreamTime(self, member: Member, history: Sequence[History]) -> int:
        """
        Calculate the time a member has streamed in a voice channel.

        :param member: The member to calculate the stream time for.
        :param history: The history of the member.
        :return: The time the member has streamed in seconds.
        """
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
