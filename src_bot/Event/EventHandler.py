from asyncio.locks import Lock

from discord import Member, VoiceState, Guild
from sqlalchemy import null, select, exists
from sqlalchemy.orm import aliased

from database.Domain.models.History import History
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Guild.GuildManager import GuildManager
from src_bot.Helpers.FunctionName import listenerName
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType
from src_bot.Types.EventHandlerListenerType import EventHandlerListenerType
from src_bot.Types.GuildListenerType import GuildListenerType

logger = Logger("EventHandler")


class EventHandler:
    _self = None

    memberLeaveListeners = []

    def __init__(self, client: Client, guildManager: GuildManager):
        self.client = client
        self.guildManager = guildManager
        self.session = getSession()
        self.lock = Lock()

        self.registerListeners()

    # Singleton pattern to ensure the lock is shared between all instances
    def __new__(cls, *args, **kwargs) -> "EventHandler":
        if not cls._self:
            cls._self = super().__new__(cls)

        return cls._self

    def addListener(self, type: EventHandlerListenerType, listener: callable):
        """
        Add a listener to the event handler.

        :param type: The type of the event handler.
        :param listener: The listener to add.
        """
        match type:
            case EventHandlerListenerType.MEMBER_LEAVE:
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

        self.guildManager.addListener(self.onBotStart, GuildListenerType.START_UP)
        logger.debug("Registered bot start listener")

        self.guildManager.addListener(self.onBotStart, GuildListenerType.GUILD_JOIN)
        logger.debug("Registered guild join listener")

    async def onBotStart(self, guild: Guild):
        """
        Refresh the history for all members in the guild.

        :param guild: The guild to refresh the history for.
        """

        def getQueryForEventWithNoClosingEvent(eventId: int, closingEventId: int):
            """
            Create a query to fetch all members that have an event with no closing event.
            """
            # noinspection PyTypeChecker
            return (
                select(History)
                .where(
                    History.guild_id == guild.id,
                    History.event_id == eventId,
                    # ~exists() is the same as NOT EXISTS
                    ~exists().where(
                        subHistory.discord_id == History.discord_id,
                        subHistory.guild_id == guild.id,
                        subHistory.event_id == closingEventId,
                        subHistory.time > History.time,
                    )
                )
                # only look at the latest history entry
                .limit(1)
            )

        with self.session:
            # rename the history table to subHistory to avoid conflicts in the subquery
            subHistory = aliased(History)

            # fetch all members that are currently online, according to the history
            currentOnlineMembersPerHistoryQuery = getQueryForEventWithNoClosingEvent(7, 8)

            didStreamQuery = getQueryForEventWithNoClosingEvent(5, 6)
            wasMutedQuery = getQueryForEventWithNoClosingEvent(1, 2)
            wasDeafenedQuery = getQueryForEventWithNoClosingEvent(3, 4)

            try:
                currentOnlineMembersPerHistory = (
                    self.session
                    .execute(currentOnlineMembersPerHistoryQuery)
                    .scalars()
                    .all()
                )
                currentOnlineMembersPerHistory = {history.discord_id:
                                                      (history.channel_id if history.channel_id else null())
                                                  for history in currentOnlineMembersPerHistory}

                # TODO maybe fetch them only if needed
                didStream = (
                    self.session
                    .execute(didStreamQuery)
                    .scalars()
                    .all()
                )
                didStream = {history.discord_id:
                                 (history.channel_id if history.channel_id else null())
                             for history in didStream}

                wasMuted = (
                    self.session
                    .execute(wasMutedQuery)
                    .scalars()
                    .all()
                )
                wasMuted = {history.discord_id:
                                (history.channel_id if history.channel_id else null())
                            for history in wasMuted}

                wasDeafened = (
                    self.session
                    .execute(wasDeafenedQuery)
                    .scalars()
                    .all()
                )
                wasDeafened = {history.discord_id:
                                   (history.channel_id if history.channel_id else null())
                               for history in wasDeafened}
            except Exception as error:
                logger.error(
                    f"Failed to get current online members per history for guild {guild.name, guild.id}",
                    exc_info=error,
                )

                return

            historiesToInsert = []
            membersThatLeft = []

            for member in guild.members:
                if member.bot:
                    continue

                # member is currently online
                if member.voice:
                    # member was tracked as online previously
                    if member.id in currentOnlineMembersPerHistory.keys():
                        # if member is in a different channel than before
                        if ((channelId := currentOnlineMembersPerHistory[member.id])
                                and channelId != member.voice.channel.id):
                            historiesToInsert.append(
                                History(
                                    discord_id=member.id,
                                    guild_id=guild.id,
                                    event_id=9,
                                    additional_info={
                                        "channel_from": channelId,
                                        "channel_to": member.voice.channel.id,
                                    },
                                )
                            )

                        continue

                    # member is currently online but was not tracked as online previously
                    historiesToInsert.append(
                        History(
                            discord_id=member.id,
                            guild_id=guild.id,
                            event_id=7,
                            channel_id=member.voice.channel.id,
                        )
                    )
                # member is currently offline but was tracked as online previously
                elif member.id in currentOnlineMembersPerHistory.keys():
                    # TODO make better logic for this
                    if member.id in didStream.keys():
                        historiesToInsert.append(
                            History(
                                discord_id=member.id,
                                guild_id=guild.id,
                                event_id=6,
                                channel_id=didStream[member.id],
                            )
                        )

                    if member.id in wasMuted.keys():
                        historiesToInsert.append(
                            History(
                                discord_id=member.id,
                                guild_id=guild.id,
                                event_id=2,
                                channel_id=wasMuted[member.id],
                            )
                        )

                    if member.id in wasDeafened.keys():
                        historiesToInsert.append(
                            History(
                                discord_id=member.id,
                                guild_id=guild.id,
                                event_id=4,
                                channel_id=wasDeafened[member.id],
                            )
                        )

                    historiesToInsert.append(
                        History(
                            discord_id=member.id,
                            guild_id=guild.id,
                            event_id=8,
                            channel_id=currentOnlineMembersPerHistory[member.id],
                        )
                    )
                    membersThatLeft.append(member)

            try:
                self.session.bulk_save_objects(historiesToInsert, preserve_order=True)
                self.session.commit()
            except Exception as error:
                logger.error(
                    f"Failed to insert histories for guild {guild.name, guild.id}",
                    exc_info=error,
                )
                self.session.rollback()

                return
            else:
                logger.debug(f"Updated histories for members in guild {guild.name, guild.id}")

            # notify listeners about members that left to invoke the leave event
            for member in membersThatLeft:
                for listener in self.memberLeaveListeners:
                    await listener(member)
                    logger.debug("Notified member leave listeners")

    async def voiceStateUpdate(self, member: Member, before: VoiceState, after: VoiceState):
        """
        Handles voice state updates for a member and saves the history to the database.

        :param member: The member that had a voice state update.
        :param before: The voice state before the update.
        :param after: The voice state after the update.
        """
        async with self.lock:
            def getHistoryObject(eventId: int, channelId: int | None = None, additionalInfo: dict | None = None):
                """
                Create a history object for the given event and additional info.

                :param eventId: The event id of the history.
                :param channelId: The channel in which the event took place.
                :param additionalInfo: Additional info for the history.
                """
                return History(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    event_id=eventId,
                    channel_id=channelId,
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
                histories.append(getHistoryObject(7, after.channel.id))

            # Member moved to another voice channel
            if before.channel and after.channel and before.channel.id != after.channel.id:
                histories.append(
                    getHistoryObject(
                        9,
                        channelId=None,
                        additionalInfo={
                            "channel_from": before.channel.id,
                            "channel_to": after.channel.id,
                        }
                    )
                )

            # Member muted themselves or was muted
            if (after.self_mute or after.mute) and not (before.self_mute or before.mute):
                histories.append(getHistoryObject(1, after.channel.id))

            # Member joined a voice channel muted
            if not before.channel and after.channel and (after.self_mute or after.mute):
                histories.append(getHistoryObject(1, after.channel.id))

            # Member unmuted themselves or was unmuted
            if not (after.self_mute or after.mute) and (before.self_mute or before.mute):
                histories.append(getHistoryObject(2, after.channel.id))

            # Member deafened themselves or was deafened
            if (after.self_deaf or after.deaf) and not (before.self_deaf or before.deaf):
                histories.append(getHistoryObject(3, after.channel.id))

            # Member joined a voice channel deafened
            if not before.channel and after.channel and (after.self_deaf or after.deaf):
                histories.append(getHistoryObject(3, after.channel.id))

            # Member undeafened themselves or was undeafened
            if not (after.self_deaf or after.deaf) and (before.self_deaf or before.deaf):
                histories.append(getHistoryObject(4, after.channel.id))

            # Member started streaming
            if (after.self_video or after.self_stream) and not (before.self_stream or before.self_video):
                histories.append(getHistoryObject(5, after.channel.id))

            # Member stopped streaming
            if not (after.self_video or after.self_stream) and (before.self_stream or before.self_video):
                histories.append(getHistoryObject(6, after.channel.id))

            # last history to save for the join-leave-circle
            # Member left a voice channel
            if before.channel and not after.channel:
                # unmute member upon leaving
                if before.self_mute or before.mute:
                    histories.append(getHistoryObject(2, before.channel.id))

                # undeafen member upon leaving
                if before.self_deaf or before.deaf:
                    histories.append(getHistoryObject(4, before.channel.id))

                # stop streaming upon leaving
                if before.self_video or before.self_stream:
                    histories.append(getHistoryObject(6, before.channel.id))

                # insert last to complete the join-leave-circle
                histories.append(getHistoryObject(8, before.channel.id))
                memberLeft = True

            if len(histories) == 0:
                logger.debug(f"No history to save for {member.display_name, member.id}")

                return

            with self.session:
                try:
                    self.session.bulk_save_objects(histories)
                    self.session.commit()
                except Exception as error:
                    logger.error(f"Failed to save histories for {member.display_name, member.id}", exc_info=error)
                    self.session.rollback()

                    return
                else:
                    logger.debug(f"Saved {len(histories)} histories for {member.display_name, member.id}")

        # TODO evaluate if this should be called within the lock
        if memberLeft:
            for listener in self.memberLeaveListeners:
                await listener(member)
                logger.debug("Notified member leave listeners")
