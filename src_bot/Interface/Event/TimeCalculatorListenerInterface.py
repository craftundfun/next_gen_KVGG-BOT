from abc import abstractmethod, ABC
from datetime import date

from discord import Member

from src_bot.Interface.Interface import Interface
from src_bot.Types.EventType import EventType


class TimeCalculatorListenerInterface(Interface, ABC):

    @abstractmethod
    async def onStatusEnd(self, member: Member, eventId: EventType, time: int, date: date):
        pass

    @abstractmethod
    async def increaseStatistic(self,
                                member: Member,
                                date: date,
                                onlineTime: int = 0,
                                muteTime: int = 0,
                                deafTime: int = 0,
                                streamTime: int = 0):
        pass

    @abstractmethod
    async def increaseActivityStatistic(self,
                                        member: Member,
                                        time: int,
                                        activityId: int,
                                        date: date, ):
        pass
