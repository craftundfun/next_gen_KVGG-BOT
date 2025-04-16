from abc import ABC, abstractmethod
from datetime import datetime

from discord import Member

from src_bot.Interface.Interface import Interface


class ActivityManagerListenerInterface(Interface, ABC):

    @abstractmethod
    async def activityStart(self, member: Member):
        pass

    @abstractmethod
    async def activitySwitch(self, before: Member, after: Member):
        pass

    @abstractmethod
    async def activityStop(self, member: Member, endtime: datetime, activityId: int):
        pass
