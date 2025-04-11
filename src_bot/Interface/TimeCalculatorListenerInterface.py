from abc import abstractmethod, ABC
from datetime import date

from discord import Member

from src_bot.Interface.Interface import Interface
from src_bot.Types.EventType import EventType


class TimeCalculatorListenerInterface(Interface, ABC):

    @abstractmethod
    async def onStatusEnd(self, member: Member, eventId: EventType, time: int, date: date):
        pass
