from abc import ABC, abstractmethod

from src_bot.Interface.Interface import Interface


class CommandSkeletonListenerInterface(Interface, ABC):

    @abstractmethod
    async def beforeCommand(self):
        pass

    @abstractmethod
    async def afterCommand(self):
        pass
