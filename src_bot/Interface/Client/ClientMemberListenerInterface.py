from abc import abstractmethod, ABC

from discord import Member, RawMemberRemoveEvent

from src_bot.Interface.Interface import Interface


class ClientMemberListenerInterface(Interface, ABC):

    @abstractmethod
    async def onMemberJoin(self, member: Member):
        pass

    @abstractmethod
    async def onMemberRemove(self, member: Member):
        pass

    @abstractmethod
    async def onMemberUpdate(self, before: Member, after: Member):
        pass

    @abstractmethod
    async def onRawMemberRemove(self, payload: RawMemberRemoveEvent):
        pass
