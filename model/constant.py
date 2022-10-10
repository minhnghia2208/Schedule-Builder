from enum import Enum
class COLUMNS(Enum):
    DATE = "*Date"
    STIME = "*Time Start"
    ETIME = "*Time End"
    SESSION_TYPE = "*Session or \nSub-session(Sub)"
    SESSION_TITLE = "*Session Title"
    ROOM = "Room/Location"
    DESCIPTION = "Description"
    SPEAKER = "Speakers"

class SESSION_TYPE(Enum):
    MAIN = "Session"
    SUB = "Sub"