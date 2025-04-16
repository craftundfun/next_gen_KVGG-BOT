from abc import ABC, abstractmethod

from discord import Member

from src_bot.Interface.Interface import Interface


class EventHandlerListenerInterface(Interface, ABC):

    @abstractmethod
    async def onMemberLeave(self, member: Member):
        pass
