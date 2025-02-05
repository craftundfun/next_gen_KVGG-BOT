from inspect import iscoroutinefunction
from typing import Any

from discord import Client as discordClient, Guild, Member, RawMemberRemoveEvent
from discord import Intents, VoiceState
from discord.abc import GuildChannel

from src_bot.Helpers.FunctionName import listenerName
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType

logger = Logger("Client")


class Client(discordClient):
    _self = None

    readyListener = []
    guildUpdate = []
    channelCreateListener = []
    channelDeleteListener = []
    guildJoinListener = []
    guildRemoveListener = []
    channelUpdateListener = []
    memberJoinListener = []
    memberRemoveListener = []
    memberRemoveListenerRaw = []
    memberUpdateListener = []
    voiceUpdateListener = []
    memberPresenceUpdateListener = []
    memberActivityUpdateListener = []

    ready = False

    def __new__(cls, *args, **kwargs) -> discordClient:
        if not cls._self:
            cls._self = super().__new__(cls)

        return cls._self

    def __init__(self, controller, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)

        self.controller = controller

    def addListener(self, listener: callable, listenerType: ClientListenerType):
        """
        Add a callable (function /) listener to a specific event

        :param listener: Callable async function
        :param listenerType: Type
        :return:
        """
        if not iscoroutinefunction(listener):
            logger.error(f"Listener is not an asynchronous function: {listener}")

            raise ValueError(f"Listener is not async")

        match listenerType:
            case ClientListenerType.READY:
                self.readyListener.append(listener)
            case ClientListenerType.GUILD_UPDATE:
                self.guildUpdate.append(listener)
            case ClientListenerType.CHANNEL_CREATE:
                self.channelCreateListener.append(listener)
            case ClientListenerType.CHANNEL_DELETE:
                self.channelDeleteListener.append(listener)
            case ClientListenerType.GUILD_JOIN:
                self.guildJoinListener.append(listener)
            case ClientListenerType.GUILD_REMOVE:
                self.guildRemoveListener.append(listener)
            case ClientListenerType.CHANNEL_UPDATE:
                self.channelUpdateListener.append(listener)
            case ClientListenerType.MEMBER_JOIN:
                self.memberJoinListener.append(listener)
            case ClientListenerType.MEMBER_REMOVE:
                self.memberRemoveListener.append(listener)
            case ClientListenerType.RAW_MEMBER_REMOVE:
                self.memberRemoveListenerRaw.append(listener)
            case ClientListenerType.MEMBER_UPDATE:
                self.memberUpdateListener.append(listener)
            case ClientListenerType.VOICE_UPDATE:
                self.voiceUpdateListener.append(listener)
            case ClientListenerType.STATUS_UPDATE:
                self.memberPresenceUpdateListener.append(listener)
            case ClientListenerType.ACTIVITY_UPDATE:
                self.memberActivityUpdateListener.append(listener)
            case _:
                logger.error(f"Invalid listener type: {listenerType}")

                raise ValueError(f"Invalid listener type: {listenerType}")

        logger.debug(f"Listener successfully added: {listenerName(listener)}")

    # TODO called multiple times, probably just live with it
    async def on_ready(self):
        """
        Notify all listeners that the bot is ready

        :return:
        """
        if self.ready:
            logger.warning("Bot is already ready")

            return

        self.ready = True

        # TODO write a wrapper for calling listeners and include error handling
        for listener in self.readyListener:
            await listener()
            logger.debug(f"Notified ready listener: {listenerName(listener)}")

    async def on_guild_update(self, before: Guild, after: Guild):
        """
        Notify all listeners that a guild has been updated

        :param before: State before the change
        :param after: State after the change
        :return:
        """
        for listener in self.guildUpdate:
            await listener(before, after)
            logger.debug(f"Notified guild update listener: {listenerName(listener)}")

    async def on_guild_channel_create(self, channel: GuildChannel):
        """
        Notify all listeners that a channel has been created

        :param channel: Channel that was created
        :return:
        """
        for listener in self.channelCreateListener:
            await listener(channel)
            logger.debug(f"Notified channel create listener: {listenerName(listener)}")

    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        """
        Notify all listeners that a channel has been updated

        :param before: Channel state before the change
        :param after: Channel state after the change
        :return:
        """
        for listener in self.channelUpdateListener:
            await listener(before, after)
            logger.debug(f"Notified channel update listener: {listenerName(listener)}")

    async def on_guild_channel_delete(self, channel: GuildChannel):
        """
        Notify all listeners that a channel has been deleted

        :param channel: Channel that was deleted
        :return:
        """
        for listener in self.channelDeleteListener:
            await listener(channel)
            logger.debug(f"Notified channel delete listener: {listenerName(listener)}")

    async def on_guild_join(self, guild: Guild):
        """
        Notify all listeners that the bot has joined a guild

        :param guild: Guild that was joined
        :return:
        """
        for listener in self.guildJoinListener:
            await listener(guild)
            logger.debug(f"Notified guild join listener: {listenerName(listener)}")

    async def on_guild_remove(self, guild: Guild):
        """
        When the bot is removed from a guild

        :param guild: Guild that was removed
        :return:
        """
        for listener in self.guildRemoveListener:
            await listener(guild)
            logger.debug(f"Notified guild remove listener: {listenerName(listener)}")

    async def on_member_join(self, member: Member):
        """
        When a member joins a guild

        :param member: Guild specific member that joined
        :return:
        """
        for listener in self.memberJoinListener:
            await listener(member)
            logger.debug(f"Notified member join listener: {listenerName(listener)}")

    async def on_member_remove(self, member: Member):
        """
        When a member leaves a guild

        :param member: Guild specific member that left
        :return:
        """
        for listener in self.memberRemoveListener:
            await listener(member)
            logger.debug(f"Notified member join listener: {listenerName(listener)}")

    async def on_raw_member_remove(self, payload: RawMemberRemoveEvent):
        """
        When a member leaves a guild and is not cached

        :param payload: Raw member remove event
        :return:
        """
        for listener in self.memberRemoveListenerRaw:
            await listener(payload)
            logger.debug(f"Notified raw member remove listener: {listenerName(listener)}")

    async def on_member_update(self, before: Member, after: Member):
        """
        When a member is updated

        :param before: Member state before the change
        :param after: Member state after the change
        :return:
        """
        for listener in self.memberUpdateListener:
            await listener(before, after)
            logger.debug(f"Notified member update listener: {listenerName(listener)}")

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        """
        When a member has a voice state update

        :param member: The member that had a voice state update.
        :param before: The voice state before the update.
        :param after: The voice state after the update.
        """
        for listener in self.voiceUpdateListener:
            await listener(member, before, after)
            logger.debug(f"Notified voice state update listener: {listenerName(listener)}")

    async def on_presence_update(self, before: Member, after: Member):
        """
        When a member has a presence update, such as status or activity change.

        :param before: The member's presence before the update.
        :param after: The member's presence after the update.
        """
        # TODO maybe look at every activity in the list
        if before.activity != after.activity:
            logger.debug(f"Activity changed for {before.display_name, before.id} "
                         f"on {before.guild.name, before.guild.id}")

            for listener in self.memberActivityUpdateListener:
                await listener(before, after)
                logger.debug(f"Notified activity update listener: {listenerName(listener)}")

        if before.status != after.status:
            logger.debug(f"Status changed for {before.display_name, before.id} on {before.guild.name, before.guild.id}")

            for listener in self.memberPresenceUpdateListener:
                await listener(before, after)
                logger.debug(f"Notified presence update listener: {listenerName(listener)}")

        # # TODO remove, its only temporary
        # from src_bot.Database.DatabaseConnection import getSession
        # from database.Domain.models.Activity import Activity
        # from database.Domain.models.ActivityHistory import ActivityHistory
        # from database.Domain.models.ActivityMapping import ActivityMapping
        # from sqlalchemy import select
        # from sqlalchemy.orm.exc import NoResultFound
#
# try:
#     with getSession() as session:
#         activityToLookAt = None
#
#         if not before.activity and after.activity:
#             activityToLookAt = after.activity
#             event = 10
#         elif before.activity and not after.activity:
#             activityToLookAt = before.activity
#             event = 11
#         # TODO if implemented correctly, watch out for game changes
#         elif before.activity != after.activity:
#             logger.warning(f"Activity changed for {before.display_name, before.id}")
#             activityToLookAt = after.activity
#             event = 10
#
#         if not activityToLookAt:
#             logger.warning(f"Nothing changed: {before.activity} -> {after.activity}")
#
#             return
#
#         selectQuery = select(Activity).where(Activity.external_activity_id == activityToLookAt.application_id, )
#
#         try:
#             activity = session.execute(selectQuery).scalars().one()
#         except NoResultFound:
#             logger.debug("creating new activity")
#
#             activity = Activity(
#                 external_activity_id=activityToLookAt.application_id,
#                 name=activityToLookAt.name,
#             )
#
#             session.add(activity)
#             # commit to trigger the trigger
#             session.commit()
#
#         selectQuery = select(ActivityMapping).where(
#             ActivityMapping.secondary_activity_id == activity.id, )
#
#         try:
#             activityMapping = session.execute(selectQuery).scalars().one()
#         except NoResultFound:
#             logger.error(f"No activity mapping found for activity {activityToLookAt}")
#
#             return
#
#         activityHistory = ActivityHistory(
#             discord_id=after.id,
#             guild_id=after.guild.id,
#             activity_id=activityMapping.primary_activity_id,
#             event_id=event,
#         )
#
#         session.add(activityHistory)
#         session.commit()
#
#         logger.debug(f"Added activity history: {activityHistory} for {after.display_name, after.id}")
# except AttributeError:
#     logger.warning("Activity has no application id, aborting")
#
#     return
# except Exception as error:
#     logger.error("Error while updating presence", exc_info=error)
