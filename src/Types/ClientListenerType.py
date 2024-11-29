from enum import Enum


class ClientListenerType(Enum):
    READY = "ready"

    GUILD_UPDATE = "guild_update"
    GUILD_JOIN = "guild_join"
    GUILD_REMOVE = "guild_remove"

    CHANNEL_CREATE = "channel_create"
    CHANNEL_DELETE = "channel_delete"
    CHANNEL_UPDATE = "channel_update"

    MEMBER_JOIN = "member_join"
