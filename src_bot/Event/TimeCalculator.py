from collections import defaultdict
from datetime import timedelta, datetime, timezone
from typing import Sequence

from discord import Member
from sqlalchemy import select

from database.Domain.models import History
from src_bot.Activity.ActivityManager import ActivityManager
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Event.EventHandler import EventHandler
from src_bot.Helpers.FunctionName import listenerName
from src_bot.Helpers.InterfaceImplementationCheck import checkInterfaceImplementation
from src_bot.Interface.ActivityManagerListenerInterface import ActivityManagerListenerInterface
from src_bot.Interface.StatusManagerListenerInterface import StatusManagerListenerInterface
from src_bot.Interface.TimeCalculatorListenerInterface import TimeCalculatorListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Member.StatusManager import StatusManager
from src_bot.Types.ActivityManagerListenerType import ActivityManagerListenerType
from src_bot.Types.EventHandlerListenerType import EventHandlerListenerType
from src_bot.Types.EventType import EventType
from src_bot.Types.StatusListenerType import StatusListenerType
from src_bot.Types.TimeCalculatorListenerType import TimeCalculatorListenerType

logger = Logger("TimeCalculator")


class TimeCalculator(StatusManagerListenerInterface, ActivityManagerListenerInterface):
    memberLeaveListeners = []
    activityStopListeners = []
    onStatusEndListeners = []

    def __init__(self, eventHandler: EventHandler, activityManager: ActivityManager, statusManager: StatusManager):
        self.eventHandler = eventHandler
        self.activityManager = activityManager
        self.statusManager = statusManager

        self.session = getSession()

        self.registerListener()

    def addListener(self, type: TimeCalculatorListenerType, listener: callable):
        """
        Add a listener to the time calculator.

        :param type: The type of the listener.
        :param listener: The listener to add.
        """
        checkInterfaceImplementation(listener, TimeCalculatorListenerInterface)

        match type:
            case TimeCalculatorListenerType.MEMBER_LEAVE:
                self.memberLeaveListeners.append(listener)
            case TimeCalculatorListenerType.ACTIVITY_STOP:
                self.activityStopListeners.append(listener)
            case TimeCalculatorListenerType.STATUS_STOP:
                self.onStatusEndListeners.append(listener)
            case _:
                logger.error(f"Unknown time calculator type {type}")

                return

        logger.debug(f"Listener successfully added: {listenerName(listener)}")

    def registerListener(self):
        """
        Register the listener for the time calculator.
        """
        self.eventHandler.addListener(EventHandlerListenerType.MEMBER_LEAVE, self.onMemberLeave)
        logger.debug("Member leave listener registered")

        self.activityManager.addListener(self.activityStop, ActivityManagerListenerType.ACTIVITY_STOP)
        logger.debug("Activity stop listener registered")

        self.statusManager.addListener(self.onStatusChange, StatusListenerType.STATUS_UPDATE)
        logger.debug("Status update listener registered")

    async def onStatusChange(self, before: Member, after: Member, eventBefore: EventType, eventAfter: EventType):
        """
        Called when a member's status changes. This includes online, idle, and dnd.
        The corresponding time of the ended event is calculated and the listeners are invoked.

        :param before: The member before the status change
        :param after: The member after the status change
        :param eventBefore: The event before the status change
        :param eventAfter: The event after the status change
        """
        selectQuery = (
            select(History)
            .where(
                History.discord_id == before.id,
                History.guild_id == before.guild.id,
                History.event_id.in_([i for i in range(EventType.ONLINE_START.value, EventType.OFFLINE_END.value + 1)]),
                # get the start event
                History.id >= (
                    select(History.id)
                    .where(History.discord_id == before.id,
                           History.guild_id == before.guild.id,
                           # for example, online_end = 13 -> we look for online start
                           History.event_id == EventType.getCorrespondingStartEvent(eventBefore).value, )
                    .order_by(History.time.desc())
                    .limit(1)
                    .scalar_subquery()
                ),
            )
            .order_by(History.id.desc())
        )

        with self.session:
            try:
                histories: list[History] = list(self.session.execute(selectQuery).scalars().all())
            except Exception as error:
                logger.error("Error while executing select query", exc_info=error)

                return

            # we only want the start and end of the ended status, and the start of the new status because why not
            if len(histories) != 3:
                # TODO raise to error and handle the case someone has no history
                logger.warning(f"Expected 3 histories, but got {len(histories)} for {before.display_name, before.id} "
                               f"on {before.guild.name, before.guild.id}")

                return

            histories = histories[1:3][::-1]
            statusSince = histories[0].time
            time = {}

            # calculate the time everyday
            while statusSince.date() < histories[1].time.date():
                midnight = datetime.combine(statusSince + timedelta(days=1), datetime.min.time())
                delta = midnight - statusSince
                time[statusSince.date()] = self._timedeltaToMicroseconds(delta)
                statusSince = midnight

            delta = histories[1].time - statusSince
            time[histories[1].time.date()] = self._timedeltaToMicroseconds(delta)

            for key in time:
                for listener in self.onStatusEndListeners:
                    try:
                        await listener(after, EventType.getCorrespondingStartEvent(eventBefore), time[key], key)
                        logger.debug(f"Invoked listener: {listenerName(listener)}")
                    except Exception as error:
                        logger.error(f"Error while invoking listener {listenerName(listener)}", exc_info=error)

                        continue

    # noinspection PyMethodMayBeStatic
    def _timedeltaToMicroseconds(self, delta: timedelta) -> int:
        """
        Returns the microseconds of a timedelta.
        """
        return delta.days * 86400 * 1_000_000 + delta.seconds * 1_000_000 + delta.microseconds

    async def activityStop(self, member: Member, endtime: datetime, activityId: int):
        """
        Calculate the time the member did the activity and invoke the listeners.

        :param member: The member that stopped the activity.
        :param endtime: The time the activity stopped.
        :param activityId: The database id of the activity.
        """
        # check whether the endtime knows the timezone
        if endtime.tzinfo is None or endtime.tzinfo.utcoffset(endtime) is None:
            logger.error("Given endtime is a naive datetime, but expected aware datetime")

            return

        async def calculateTimeAndNotifyListeners(time: timedelta, date: datetime.date):
            timeInMicroseconds = self._timedeltaToMicroseconds(time)

            for listener in self.activityStopListeners:
                await listener(member, timeInMicroseconds, activityId, date)
                logger.debug(f"Invoked listener: {listenerName(listener)}")

        startTime = member.activity.created_at

        # the activity happened on the same day
        if startTime.date() == endtime.date():
            logger.debug(f"f{member.display_name, member.id} played the activity {activityId} on "
                         f"{member.guild.name, member.guild.id} on the same day")

            await calculateTimeAndNotifyListeners(endtime - startTime, endtime.date())

            return

        days = (endtime.date() - startTime.date()).days

        # first day
        midnight = datetime.combine(startTime.date() + timedelta(days=1), datetime.min.time())
        midnight = midnight.replace(tzinfo=timezone.utc)

        await calculateTimeAndNotifyListeners(midnight - startTime, startTime.date())

        # days in between if there are any
        for i in range(1, days):
            midnight = datetime.combine(startTime.date() + timedelta(days=i + 1), datetime.min.time())
            midnight = midnight.replace(tzinfo=timezone.utc)

            await calculateTimeAndNotifyListeners((timedelta(days=1)), startTime.date() + timedelta(days=i))

        # last day
        await calculateTimeAndNotifyListeners(endtime - midnight, endtime.date())

    # noinspection PyMethodMayBeStatic
    def calculateTimesPerDay(self, member: Member, history: Sequence[History]) -> dict | None:
        """
        Calculate the online, mute and stream times per day.

        :param member: Member to calculate the times for, but this is only needed for logging.
        :param history: History of the member.
        :return: Dictionary with the times per day.
        """
        if not history:
            logger.error(f"No history given for {member.display_name, member.id} "
                         f"on {member.guild.name, member.guild.id}")
            return None

        # dictionary with the times per day and a default value of 0
        dailyTimes = defaultdict(lambda: {"online": 0, "mute": 0, "deaf": 0, "stream": 0})

        onlineSince: datetime = history[0].time

        # list of tuples with the start and end time of the mute and stream intervals
        muteIntervals: list[tuple[datetime, datetime]] = []
        streamIntervals: list[tuple[datetime, datetime]] = []
        deafIntervals: list[tuple[datetime, datetime]] = []

        muteActive: datetime | None = None
        streamActive: datetime | None = None
        deafActive: datetime | None = None

        for event in history:
            # mute
            if event.event_id == 1:
                muteActive = event.time
            # unmute
            elif event.event_id == 2 and muteActive:
                muteIntervals.append((muteActive, event.time))
                muteActive = None
            # deaf
            elif event.event_id == 3:
                deafActive = event.time
            # undeaf
            elif event.event_id == 4 and deafActive:
                deafIntervals.append((deafActive, event.time))
                deafActive = None
            # stream start
            elif event.event_id == 5:
                streamActive = event.time
            # stream end
            elif event.event_id == 6 and streamActive:
                streamIntervals.append((streamActive, event.time))
                streamActive = None

        endTime: datetime = history[-1].time

        while onlineSince.date() < endTime.date():
            midnight = datetime.combine(onlineSince.date() + timedelta(days=1), datetime.min.time())
            delta = midnight - onlineSince
            dailyTimes[onlineSince.date()]["online"] += self._timedeltaToMicroseconds(delta)
            onlineSince = midnight

        # add the time left until the last event
        delta = endTime - onlineSince
        dailyTimes[endTime.date()]["online"] += self._timedeltaToMicroseconds(delta)

        # TODO perhaps outsource it to a function?
        for start, end in muteIntervals:
            current = start

            while current.date() < end.date():
                midnight = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
                delta = midnight - current
                dailyTimes[current.date()]["mute"] += self._timedeltaToMicroseconds(delta)
                current = midnight

            delta = end - current
            dailyTimes[end.date()]["mute"] += self._timedeltaToMicroseconds(delta)

        for start, end in deafIntervals:
            current = start

            while current.date() < end.date():
                midnight = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
                delta = midnight - current
                dailyTimes[current.date()]["deaf"] += self._timedeltaToMicroseconds(delta)
                current = midnight

            delta = end - current
            dailyTimes[end.date()]["deaf"] += self._timedeltaToMicroseconds(delta)

        for start, end in streamIntervals:
            current = start

            while current.date() < end.date():
                midnight = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
                delta = midnight - current
                dailyTimes[current.date()]["stream"] += self._timedeltaToMicroseconds(delta)
                current = midnight

            delta = end - current
            dailyTimes[end.date()]["stream"] += self._timedeltaToMicroseconds(delta)

        return dict(dailyTimes)

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

            if not history:
                logger.error(f"No history found for {member.display_name, member.id} "
                             f"on {member.guild.name, member.guild.id}")

                return

            times = self.calculateTimesPerDay(member, history)

        # TODO maybe do this in another way?
        for listener in self.memberLeaveListeners:
            for key in times:
                onlineTime = times[key]["online"]
                muteTime = times[key]["mute"]
                deafTime = times[key]["deaf"]
                streamTime = times[key]["stream"]

                await listener(member, key, onlineTime, muteTime, deafTime, streamTime, )
                logger.debug(f"Invoked listener: {listenerName(listener)}")

    async def activityStart(self, member: Member):
        pass

    async def activitySwitch(self, before: Member, after: Member):
        pass
