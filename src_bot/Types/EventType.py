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

    @classmethod
    def getCorrespondingStartEvent(cls, startEvent: "EventType") -> "EventType":
        match startEvent:
            case EventType.UNMUTE:
                return EventType.MUTE
            case EventType.UNDEAF:
                return EventType.DEAF
            case EventType.STREAM_END:
                return EventType.STREAM_START
            case EventType.VOICE_LEAVE:
                return EventType.VOICE_JOIN
            case EventType.ACTIVITY_END:
                return EventType.ACTIVITY_START
            case EventType.ONLINE_END:
                return EventType.ONLINE_START
            case EventType.IDLE_END:
                return EventType.IDLE_START
            case EventType.DND_END:
                return EventType.DND_START
            case EventType.OFFLINE_END:
                return EventType.OFFLINE_START
            case _:
                raise ValueError(f"Unknown event type or this event has no start: {self}")
