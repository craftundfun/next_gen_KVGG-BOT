from collections import defaultdict
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

    def calculate_online_time(self, member, history):
        """
        Calculate the online, mute, and stream time of a member per day.
        :param member: The member to calculate the time for.
        :param history: The history of the member.
        :return: A dictionary with daily online, mute, and stream times in seconds.
        """
        if not history:
            return {}

        daily_times = defaultdict(lambda: {"online": 0, "mute": 0, "stream": 0})
        online_since = history[0].time
        mute_intervals = []
        stream_intervals = []

        mute_active = None
        stream_active = None

        for event in history:
            if event.event_id == 1:  # Mute
                mute_active = event.time
            elif event.event_id == 2 and mute_active:  # Unmute
                mute_intervals.append((mute_active, event.time))
                mute_active = None
            elif event.event_id == 5:  # Stream Start
                stream_active = event.time
            elif event.event_id == 6 and stream_active:  # Stream End
                stream_intervals.append((stream_active, event.time))
                stream_active = None

        end_time = history[-1].time

        while online_since.date() < end_time.date():
            midnight = datetime.combine(online_since.date() + timedelta(days=1), datetime.min.time())
            daily_times[online_since.date()]["online"] += int((midnight - online_since).total_seconds())
            online_since = midnight
        daily_times[end_time.date()]["online"] += int((end_time - online_since).total_seconds())

        for start, end in mute_intervals:
            current = start
            while current.date() < end.date():
                midnight = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
                daily_times[current.date()]["mute"] += int((midnight - current).total_seconds())
                current = midnight
            daily_times[end.date()]["mute"] += int((end - current).total_seconds())

        for start, end in stream_intervals:
            current = start
            while current.date() < end.date():
                midnight = datetime.combine(current.date() + timedelta(days=1), datetime.min.time())
                daily_times[current.date()]["stream"] += int((midnight - current).total_seconds())
                current = midnight
            daily_times[end.date()]["stream"] += int((end - current).total_seconds())

        return daily_times

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

            print(self.calculate_online_time(history))

            return

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
