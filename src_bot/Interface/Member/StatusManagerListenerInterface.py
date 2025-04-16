from abc import abstractmethod, ABC

from discord import Member

from src_bot.Interface.Interface import Interface
from src_bot.Types.EventType import EventType


# TODO implement this everywhere
class StatusManagerListenerInterface(Interface, ABC):

    @abstractmethod
    async def onStatusChange(self, before: Member, after: Member, eventBefore: EventType, eventAfter: EventType):
        pass
