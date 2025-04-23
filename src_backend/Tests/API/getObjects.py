from datetime import datetime
from itertools import product

from database.Domain import DiscordUser, WebsiteRole
from database.Domain.models import WebsiteRoleUserMapping, Event, Guild, Category, Channel, GuildDiscordUserMapping, \
    History, Statistic
from database.Domain.models import WebsiteUser
from database.Domain.models.Activity import Activity
from database.Domain.models.ActivityHistory import ActivityHistory
from database.Domain.models.ActivityStatistic import ActivityStatistic
from database.Domain.models.StatusStatistic import StatusStatistic

"""
PRESERVE THE ORDER OF THE FUNCTIONS, OTHERWISE THE KEY CONSTRAINTS WILL NOT BE MET
"""


def getGuilds():
    for i in range(3):
        yield Guild(
            guild_id=i,
            name=f"GuildNr.{i}",
            joined_at=datetime.now(),
            icon=f"<ICON>",
        )


def getDiscordUsers():
    for i in range(10):
        yield DiscordUser(
            discord_id=i,
            global_name=f"DiscordUserNr.{i}",
            created_at=datetime.now(),
        )


def getWebsiteUsers():
    for i in range(10):
        yield WebsiteUser(
            discord_id=i,
            created_at=datetime.now(),
            email=f"<EMAIL>",
        )


def getActivities():
    # if we start at 0 the auto_increment will take over and we will have an integrity error
    for i in range(1, 11):
        yield Activity(
            id=i,
            external_activity_id=i,
            name=f"ActivityNr.{i}",
        )


def getEvents():
    types = [
        "MUTE",
        "UNMUTE",
        "DEAF",
        "UNDEAF",
        "STREAM_START",
        "STREAM_END",
        "VOICE_JOIN",
        "VOICE_LEAVE",
        "VOICE_CHANGE",
        "ACTIVITY_START",
        "ACTIVITY_END",
        "ONLINE_START",
        "ONLINE_END",
        "IDLE_START",
        "IDLE_END",
        "DND_START",
        "DND_END",
        "OFFLINE_START",
        "OFFLINE_END",
    ]

    for i in range(1, 20):
        yield Event(
            id=i,
            type=types[i - 1],
        )


def getActivityHistory():
    events = list(getEvents())
    events = [events[10], events[11], ]

    for activity, discordUser, guild, event in product(
            list(getActivities()),
            list(getDiscordUsers()),
            list(getGuilds()),
            events,
    ):
        yield ActivityHistory(
            discord_id=discordUser.discord_id,
            guild_id=guild.guild_id,
            primary_activity_id=activity.id,
            event_id=event.id,
            time=datetime.now(),
        )


# TODO implement things in the future if needed
def getActivityMappings():
    return []


def getActivityStatistics():
    for activity, discordUser, guild in product(
            list(getActivities()),
            list(getDiscordUsers()),
            list(getGuilds()),
    ):
        yield ActivityStatistic(
            discord_id=discordUser.discord_id,
            guild_id=guild.guild_id,
            activity_id=activity.id,
            date=datetime.now(),
            time=discordUser.discord_id + guild.guild_id + activity.external_activity_id,
        )


# def getBackendAccess():
#     pass

def getBoost():
    return []


def getCategories():
    for guild in getGuilds():
        for i in range(3):
            yield Category(
                category_id=i,
                name=f"CategoryNr.{i}",
                guild_id=guild.guild_id,
            )


def getChannels():
    for guild in getGuilds():
        for i, type in product(list(range(5)), ["text", "voice"]):
            yield Channel(
                channel_id=i,
                name=f"ChannelNr.{i}",
                type=type,
                guild_id=guild.guild_id,
            )


def getChannelSettings():
    return []


def getExperiences():
    return []


def getExperienceAmounts():
    return []


def getGuildDiscordUserMappings():
    for discordUser, guild in product(
            list(getDiscordUsers()),
            list(getGuilds()),
    ):
        yield GuildDiscordUserMapping(
            guild_id=guild.guild_id,
            discord_id=discordUser.discord_id,
            display_name=f"{discordUser.global_name}#{discordUser.discord_id}",
            joined_at=datetime.now(),
            profile_picture=f"<PROFILE_PICTURE>",
        )


def getHistories():
    # TODO better event selection
    events = list(getEvents())
    events = [events[7], events[1], events[2], events[8], ]
    i = 1

    for discordUser, guild, event, channel in product(
            list(getDiscordUsers()),
            list(getGuilds()),
            events,
            [channel for channel in list(getChannels()) if channel.type == "voice"],
    ):
        yield History(
            id=i,
            discord_id=discordUser.discord_id,
            guild_id=guild.guild_id,
            event_id=event.id,
            time=datetime.now(),
            channel_id=channel.channel_id,
        )

        i += 1


def getStatistics():
    for discordUser, guild in product(
            list(getDiscordUsers()),
            list(getGuilds()),
    ):
        yield Statistic(
            discord_id=discordUser.discord_id,
            guild_id=guild.guild_id,
            date=datetime.now(),
            online_time=(discordUser.discord_id + guild.guild_id) * 10,
            stream_time=(discordUser.discord_id + guild.guild_id) * 5,
            mute_time=(discordUser.discord_id + guild.guild_id) * 2,
            deaf_time=(discordUser.discord_id + guild.guild_id) * 3,
            message_count=(discordUser.discord_id + guild.guild_id) * 20,
            command_count=(discordUser.discord_id + guild.guild_id) * 15,
        )


def getStatusStatistics():
    for discordUser, guild in product(
            list(getDiscordUsers()),
            list(getGuilds()),
    ):
        yield StatusStatistic(
            discord_id=discordUser.discord_id,
            guild_id=guild.guild_id,
            date=datetime.now(),
            online_time=(discordUser.discord_id + guild.guild_id) * 10,
            idle_time=(discordUser.discord_id + guild.guild_id) * 5,
            dnd_time=(discordUser.discord_id + guild.guild_id) * 2,
        )


def getWebsiteRoles():
    for i, name in enumerate(["Administrator", "Moderator", "User"]):
        yield WebsiteRole(
            role_id=i,
            role_name=name,
            created_at=datetime.now(),
        )


def getWebsiteRoleUserMappings():
    # TODO create users without enough privileges
    for discordUser, websiteRole in product(list(getDiscordUsers()), list(getWebsiteRoles())):
        yield WebsiteRoleUserMapping(
            role_id=websiteRole.role_id,
            discord_id=discordUser.discord_id,
            created_at=datetime.now(),
        )
