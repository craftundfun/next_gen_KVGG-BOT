from enum import Enum


class TimeCalculatorListenerType(Enum):
    MEMBER_LEAVE = "member_leave"
    ACTIVITY_STOP = "activity_stop"
    STATUS_STOP = "status_stop"
