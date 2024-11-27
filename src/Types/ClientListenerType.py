from enum import Enum


class ClientListenerType(Enum):
    READY = "ready"
    GUILD_UPDATE = "guild_update"
    CHANNEL_CREATE = "channel_create"
    CHANNEL_DELETE = "channel_delete"
    GUILD_JOIN = "guild_join"
    GUILD_REMOVE = "guild_remove"
