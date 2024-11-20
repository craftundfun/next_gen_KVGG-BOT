from enum import Enum


class ClientListenerType(Enum):
    READY = "ready"
    GUILD_UPDATE = "guild_update"
