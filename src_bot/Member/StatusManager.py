from discord import Member, Status

from database.Domain.models import History
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Helpers.FunctionName import listenerName
from src_bot.Helpers.InterfaceImplementationCheck import checkInterfaceImplementation
from src_bot.Interface.StatusManagerListenerInterface import StatusManagerListenerInterface
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType
from src_bot.Types.EventType import EventType
from src_bot.Types.StatusListenerType import StatusListenerType

logger = Logger("StatusManager")


class StatusManager:
    statusChangeListener = []

    def __init__(self, client: Client):
        self.client = client

        self.session = getSession()

        self.registerListeners()

    def registerListeners(self):
        self.client.addListener(self.onStatusUpdate, ClientListenerType.STATUS_UPDATE)

    def addListener(self, listener: callable, listenerType: StatusListenerType):
        """
        Add a callable (function /) listener to a specific event

        :param listener: Callable async function
        :param listenerType: Type
        :return:
        """
        checkInterfaceImplementation(listener, StatusManagerListenerInterface)

        match listenerType:
            case StatusListenerType.STATUS_UPDATE:
                self.statusChangeListener.append(listener)
            case _:
                logger.error(f"Unknown listener type: {listenerName(listener)}")

    async def onStatusUpdate(self, before: Member, after: Member):
        """
        Called when a member's status changes. This includes online, idle, dnd, and offline.
        The corresponding event is saved to the database.

        :param before: The member before the status change
        :param after: The member after the status change
        """
        with self.session:
            match before.status:
                case Status.online:
                    eventIdBefore = EventType.ONLINE_END
                case Status.idle:
                    eventIdBefore = EventType.IDLE_END
                case Status.dnd:
                    eventIdBefore = EventType.DND_END
                case Status.offline:
                    eventIdBefore = EventType.OFFLINE_END
                case _:
                    logger.error(f"Unknown status: {before.status} for {before.display_name, before.id}")

                    return

            beforeHistory = History(
                discord_id=before.id,
                guild_id=before.guild.id,
                event_id=eventIdBefore.value,
            )

            match after.status:
                case Status.online:
                    eventIdAfter = EventType.ONLINE_START
                case Status.idle:
                    eventIdAfter = EventType.IDLE_START
                case Status.dnd:
                    eventIdAfter = EventType.DND_START
                case Status.offline:
                    eventIdAfter = EventType.OFFLINE_START
                case _:
                    logger.error(f"Unknown status: {after.status} for {after.display_name, after.id}")

                    return

            afterHistory = History(
                discord_id=after.id,
                guild_id=after.guild.id,
                event_id=eventIdAfter.value,
            )

            try:
                self.session.bulk_save_objects([beforeHistory, afterHistory], preserve_order=True)
                self.session.commit()
            except Exception as error:
                logger.error(f"Couldn't save status changes for {after.display_name, after.id}", exc_info=error)

                self.session.rollback()
            else:
                logger.debug(f"Saved status changes for {after.display_name, after.id} "
                             f"on {after.guild.name, after.guild.id}")

            for listener in self.statusChangeListener:
                await listener(before, after, eventIdBefore, eventIdAfter)
                logger.debug(f"Notified status change listener: {listenerName(listener)}")
