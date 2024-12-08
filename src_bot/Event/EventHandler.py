from discord import Member, VoiceState

from database.Domain.models.History import History
from src_bot.Client.Client import Client
from src_bot.Database.DatabaseConnection import getSession
from src_bot.Logging.Logger import Logger
from src_bot.Types.ClientListenerType import ClientListenerType

logger = Logger("EventHandler")


class EventHandler:

    def __init__(self, client: Client):
        self.client = client
        self.session = getSession()

        self.registerListeners()

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
        if member.bot:
            logger.debug(f"{member.display_name} is a bot, ignoring")

            return

        histories = []

        # Member joined a voice channel
        if not before.channel and after.channel:
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=7,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            # insert first to complete the join-leave-circle
            histories.append(history)

        # Member moved to another voice channel
        if before.channel and after.channel and before.channel.id != after.channel.id:
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=9,
                additional_info={
                    "channel_from": before.channel.id,
                    "channel_to": after.channel.id,
                },
            )

            histories.append(history)

        # Member left a voice channel
        if before.channel and not after.channel:
            historyLeave = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=8,
                additional_info={
                    "channel_id": before.channel.id,
                },
            )

            # unmute member upon leaving
            if before.self_mute or before.mute:
                history = History(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    event_id=2,
                    additional_info={
                        "channel_id": before.channel.id,
                    },
                )

                histories.append(history)

            # undeafen member upon leaving
            if before.self_deaf or before.deaf:
                history = History(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    event_id=4,
                    additional_info={
                        "channel_id": before.channel.id,
                    },
                )

                histories.append(history)

            # stop streaming upon leaving
            if before.self_video or before.self_stream:
                history = History(
                    discord_id=member.id,
                    guild_id=member.guild.id,
                    event_id=6,
                    additional_info={
                        "channel_id": before.channel.id,
                    },
                )

                histories.append(history)

            # insert last to complete the join-leave-circle
            histories.append(historyLeave)

        # Member muted themselves or was muted
        if (after.self_mute or after.mute) and not (before.self_mute or before.mute):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=1,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member joined a voice channel muted
        if not before.channel and after.channel and (after.self_mute or after.mute):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=1,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member unmuted themselves or was unmuted
        if not (after.self_mute or after.mute) and (before.self_mute or before.mute):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=2,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member deafened themselves or was deafened
        if (after.self_deaf or after.deaf) and not (before.self_deaf or before.deaf):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=3,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member joined a voice channel deafened
        if not before.channel and after.channel and (after.self_deaf or after.deaf):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=3,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member undeafened themselves or was undeafened
        if not (after.self_deaf or after.deaf) and (before.self_deaf or before.deaf):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=4,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member started streaming
        if (after.self_video or after.self_stream) and not (before.self_stream or before.self_video):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=5,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

        # Member stopped streaming
        if not (after.self_video or after.self_stream) and (before.self_stream or before.self_video):
            history = History(
                discord_id=member.id,
                guild_id=member.guild.id,
                event_id=6,
                additional_info={
                    "channel_id": after.channel.id,
                },
            )

            histories.append(history)

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
