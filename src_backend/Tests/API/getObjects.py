from datetime import datetime, timedelta
from functools import lru_cache
from itertools import product, count

from database.Domain import DiscordUser, WebsiteRole
from database.Domain.models import WebsiteRoleUserMapping, Event, Guild, Category, Channel, GuildDiscordUserMapping, \
    History, Statistic
from database.Domain.models import WebsiteUser
from database.Domain.models.Activity import Activity
from database.Domain.models.ActivityHistory import ActivityHistory
from database.Domain.models.ActivityStatistic import ActivityStatistic
from database.Domain.models.StatusStatistic import StatusStatistic

guildIdGenerator = count(start=1)
discordUserIdGenerator = count(start=1)
websiteUserIdGenerator = count(start=1)
activityIdGenerator = count(start=1)
categoryIdGenerator = count(start=1)
channelIdGenerator = count(start=1)


@lru_cache(maxsize=None)
def getGuilds():
    temp = []

    for _ in range(3):
        temp.append(
            Guild(
                guild_id=(i := next(guildIdGenerator)),
                name=f"GuildNr.{i}",
                joined_at=datetime.now(),
                icon=f"<ICON>",
            )
        )

    return temp


@lru_cache(maxsize=None)
def getDiscordUsers():
    temp = []

    for _ in range(10):
        temp.append(
            DiscordUser(
                discord_id=(i := next(discordUserIdGenerator)),
                global_name=f"DiscordUserNr.{i}",
                created_at=datetime.now(),
            )
        )

    return temp


@lru_cache(maxsize=None)
def getWebsiteUsers():
    temp = []

    for _ in range(10):
        temp.append(
            WebsiteUser(
                discord_id=next(websiteUserIdGenerator),
                created_at=datetime.now(),
                email=f"<EMAIL>",
            )
        )

    return temp


@lru_cache(maxsize=None)
def getActivities():
    temp = []

    for _ in range(10):
        temp.append(
            Activity(
                id=(i := next(activityIdGenerator)),
                external_activity_id=i,
                name=f"ActivityNr.{i}",
            )
        )

    return temp


def getEvents():
    temp = []
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
        temp.append(
            Event(
                id=i,
                type=types[i - 1],
            )
        )

    return temp


def getActivityHistory():
    temp = []

    events = getEvents()
    events = [events[10], events[11], ]

    for activity, discordUser, guild, event in product(
            getActivities(),
            getDiscordUsers(),
            getGuilds(),
            events,
    ):
        temp.append(
            ActivityHistory(
                discord_id=discordUser.discord_id,
                guild_id=guild.guild_id,
                primary_activity_id=activity.id,
                event_id=event.id,
                time=datetime.now(),
            )
        )

    return temp


# TODO implement things in the future if needed
def getActivityMappings():
    return []


def getActivityStatistics():
    temp = []

    for activity, discordUser, guild in product(
            getActivities(),
            getDiscordUsers(),
            getGuilds(),
    ):
        temp.append(
            ActivityStatistic(
                discord_id=discordUser.discord_id,
                guild_id=guild.guild_id,
                activity_id=activity.id,
                date=datetime.now(),
                time=discordUser.discord_id + guild.guild_id + activity.external_activity_id,
            )
        )

    return temp


# def getBackendAccess():
#     pass

def getBoost():
    return []


@lru_cache(maxsize=None)
def getCategories():
    temp = []

    for guild in getGuilds():
        for _ in range(3):
            temp.append(
                Category(
                    category_id=(i := next(categoryIdGenerator)),
                    name=f"CategoryNr.{i}",
                    guild_id=guild.guild_id,
                )
            )

    return temp


@lru_cache(maxsize=None)
def getChannels():
    temp = []

    for guild in getGuilds():
        for type in ["text", "voice"]:
            temp.append(
                Channel(
                    channel_id=(i := next(channelIdGenerator)),
                    name=f"ChannelNr.{i}",
                    type=type,
                    guild_id=guild.guild_id,
                )
            )

    return temp


def getChannelSettings():
    return []


def getExperiences():
    return []


def getExperienceAmounts():
    return []


def getGuildDiscordUserMappings():
    temp = []

    for discordUser, guild in product(
            getDiscordUsers(),
            getGuilds(),
    ):
        temp.append(
            GuildDiscordUserMapping(
                guild_id=guild.guild_id,
                discord_id=discordUser.discord_id,
                display_name=f"{discordUser.global_name}#{discordUser.discord_id}",
                joined_at=datetime.now(),
                profile_picture=f"<PROFILE_PICTURE>",
            )
        )

    return temp


def getHistories():
    # TODO better event selection
    temp = []
    events = getEvents()
    events = [events[7], events[1], events[2], events[8], ]
    i = 1

    for discordUser, guild, event, channel in product(
            getDiscordUsers(),
            getGuilds(),
            events,
            [channel for channel in getChannels() if channel.type == "voice"],
    ):
        temp.append(
            History(
                id=i,
                discord_id=discordUser.discord_id,
                guild_id=guild.guild_id,
                event_id=event.id,
                time=datetime.now(),
                channel_id=channel.channel_id,
            )
        )

        i += 1

    return temp


def getStatistics():
    temp = []

    for discordUser, guild in product(
            getDiscordUsers(),
            getGuilds(),
    ):
        temp.append(
            Statistic(
                discord_id=discordUser.discord_id,
                guild_id=guild.guild_id,
                date=datetime.now() - timedelta(days=2),
                online_time=(discordUser.discord_id + guild.guild_id) * 10,
                stream_time=(discordUser.discord_id + guild.guild_id) * 5,
                mute_time=(discordUser.discord_id + guild.guild_id) * 2,
                deaf_time=(discordUser.discord_id + guild.guild_id) * 3,
                message_count=(discordUser.discord_id + guild.guild_id) * 20,
                command_count=(discordUser.discord_id + guild.guild_id) * 15,
            )
        )

    return temp


def getStatusStatistics():
    temp = []

    for discordUser, guild in product(
            getDiscordUsers(),
            getGuilds(),
    ):
        temp.append(
            StatusStatistic(
                discord_id=discordUser.discord_id,
                guild_id=guild.guild_id,
                date=datetime.now(),
                online_time=(discordUser.discord_id + guild.guild_id) * 10,
                idle_time=(discordUser.discord_id + guild.guild_id) * 5,
                dnd_time=(discordUser.discord_id + guild.guild_id) * 2,
            )
        )

    return temp


def getWebsiteRoles():
    temp = []

    for i, name in enumerate(["Administrator", "Moderator", "User"], start=1):
        temp.append(
            WebsiteRole(
                role_id=i,
                role_name=name,
                created_at=datetime.now(),
            )
        )

    return temp


def getWebsiteRoleUserMappings():
    # TODO create users without enough privileges
    temp = []

    for discordUser, websiteRole in product(getDiscordUsers(), getWebsiteRoles()):
        temp.append(
            WebsiteRoleUserMapping(
                role_id=websiteRole.role_id,
                discord_id=discordUser.discord_id,
                created_at=datetime.now(),
            )
        )

    return temp
