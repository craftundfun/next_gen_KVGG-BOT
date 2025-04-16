from enum import Enum


class ActivityManagerListenerType(Enum):
    ACTIVITY_START = "activity_start"
    ACTIVITY_SWITCH = "activity_switch"
    ACTIVITY_STOP = "activity_stop"
