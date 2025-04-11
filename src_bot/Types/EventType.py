from enum import Enum


class EventType(Enum):
    MUTE = 1
    UNMUTE = 2
    DEAF = 3
    UNDEAF = 4
    STREAM_START = 5
    STREAM_END = 6
    VOICE_JOIN = 7
    VOICE_LEAVE = 8
    VOICE_CHANGE = 9
    ACTIVITY_START = 10
    ACTIVITY_END = 11
    ONLINE_START = 12
    ONLINE_END = 13
    IDLE_START = 14
    IDLE_END = 15
    DND_START = 16
    DND_END = 17
    OFFLINE_START = 18
    OFFLINE_END = 19
