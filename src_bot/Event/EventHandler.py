from discord import Member, VoiceState

from asyncio.locks import Lock
from database.Domain.models.History import History
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Helpers.FunctionName import listenerName
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType

from sqlalchemy import null

from src_bot.Types.EventHandlerType import EventHandlerType

logger = Logger("EventHandler")


class EventHandler:
    _self = None

    memberLeaveListeners = []

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()
        self.lock = Lock()

        self.registerListeners()

    # Singleton pattern to ensure the lock is shared between all instances
    def __new__(cls, *args, **kwargs) -> "EventHandler":
        if not cls._self:
            cls._self = super().__new__(cls)

        return cls._self

    def addListener(self, type: EventHandlerType, listener: callable):
        """
        Add a listener to the event handler.

        :param type: The type of the event handler.
        :param listener: The listener to add.
        """
        match type:
            case EventHandlerType.MEMBER_LEAVE:
                self.memberLeaveListeners.append(listener)
            case _:
                logger.error(f"Unknown event handler type {type}")

                return

        logger.debug(f"Listener successfully added: {listenerName(listener)}")

    def registerListeners(self):
        """
        Register the listeners for the event handler.
        """
        self.client.addListener(self.voiceStateUpdate, ClientListenerType.VOICE_UPDATE)
        logger.debug("Registered voice state update listener")

    # TODO startup check and periodic check if state is consistent with database
    async def voiceStateUpdate(self, member: Member, before: VoiceState, after: VoiceState):
        """
        Handles voice state updates for a member and saves the history to the database.

        :param member: The member that had a voice state update.
        :param before: The voice state before the update.
        :param after: The voice state after the update.
        """
        async with self.lock:
            def getHistoryObject(eventId: int, additionalInfo: dict | None):
                """
                Create a history object for the given event and additional info.

                :param eventId: The event id of the history.
                :param additionalInfo: Additional info for the history.
                """
                return History(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    event_id=eventId,
                    additional_info=additionalInfo if additionalInfo else null(),
                )

            if member.bot:
                logger.debug(f"{member.display_name} is a bot, ignoring")

                return

            memberLeft = False
            histories = []

            # insert first to complete the join-leave-circle
            # Member joined a voice channel
            if not before.channel and after.channel:
                histories.append(getHistoryObject(7, {"channel_id": after.channel.id}))

            # Member moved to another voice channel
            if before.channel and after.channel and before.channel.id != after.channel.id:
                histories.append(
                    getHistoryObject(9, {"channel_from": before.channel.id, "channel_to": after.channel.id}))

            # Member muted themselves or was muted
            if (after.self_mute or after.mute) and not (before.self_mute or before.mute):
                histories.append(getHistoryObject(1, {"channel_id": after.channel.id}))

            # Member joined a voice channel muted
            if not before.channel and after.channel and (after.self_mute or after.mute):
                histories.append(getHistoryObject(1, {"channel_id": after.channel.id}))

            # Member unmuted themselves or was unmuted
            if not (after.self_mute or after.mute) and (before.self_mute or before.mute):
                histories.append(getHistoryObject(2, {"channel_id": after.channel.id}))

            # Member deafened themselves or was deafened
            if (after.self_deaf or after.deaf) and not (before.self_deaf or before.deaf):
                histories.append(getHistoryObject(3, {"channel_id": after.channel.id}))

            # Member joined a voice channel deafened
            if not before.channel and after.channel and (after.self_deaf or after.deaf):
                histories.append(getHistoryObject(3, {"channel_id": after.channel.id}))

            # Member undeafened themselves or was undeafened
            if not (after.self_deaf or after.deaf) and (before.self_deaf or before.deaf):
                histories.append(getHistoryObject(4, {"channel_id": after.channel.id}))

            # Member started streaming
            if (after.self_video or after.self_stream) and not (before.self_stream or before.self_video):
                histories.append(getHistoryObject(5, {"channel_id": after.channel.id}))

            # Member stopped streaming
            if not (after.self_video or after.self_stream) and (before.self_stream or before.self_video):
                histories.append(getHistoryObject(6, {"channel_id": after.channel.id}))

            # last history to save for the join-leave-circle
            # Member left a voice channel
            if before.channel and not after.channel:
                historyLeave = getHistoryObject(8, {"channel_id": before.channel.id, })

                # unmute member upon leaving
                if before.self_mute or before.mute:
                    histories.append(getHistoryObject(2, {"channel_id": before.channel.id}))

                # undeafen member upon leaving
                if before.self_deaf or before.deaf:
                    histories.append(getHistoryObject(4, {"channel_id": before.channel.id}))

                # stop streaming upon leaving
                if before.self_video or before.self_stream:
                    histories.append(getHistoryObject(6, {"channel_id": before.channel.id}))

                # insert last to complete the join-leave-circle
                histories.append(historyLeave)
                memberLeft = True

            if len(histories) == 0:
                logger.debug(f"No history to save for {member.display_name, member.id}")

                return

            with self.session:
                for history in histories:
                    try:
                        self.session.add(history)
                    except Exception as error:
                        logger.error(f"Failed to save history for {member.display_name, member.id}", exc_info=error)

                        continue

                try:
                    self.session.commit()
                except Exception as error:
                    logger.error(f"Failed to save histories for {member.display_name, member.id}", exc_info=error)

                    self.session.rollback()
                else:
                    logger.debug(f"Saved {len(histories)} histories for {member.display_name, member.id}")

        # TODO evaluate if this should be called within the lock
        if memberLeft:
            for listener in self.memberLeaveListeners:
                await listener(member)
                logger.debug("Notified member leave listeners")
