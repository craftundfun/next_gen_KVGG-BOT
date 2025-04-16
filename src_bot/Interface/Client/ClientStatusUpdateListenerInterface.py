from abc import ABC, abstractmethod

from discord import Member, VoiceState

from src_bot.Interface.Interface import Interface


class ClientStatusUpdateListenerInterface(Interface, ABC):

    @abstractmethod
    async def onVoiceStateUpdate(self, member: Member, before: VoiceState, after: VoiceState):
        pass

    @abstractmethod
    async def onPresenceUpdate(self, before: Member, after: Member):
        pass
