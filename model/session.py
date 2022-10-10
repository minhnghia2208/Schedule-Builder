from asyncio.windows_events import NULL
from datetime import date


class Session:
    def __init__(self, id, type, date, time_start, time_end, title = None, description = None, main_session_id = None):
        self.id = id
        self.type = type
        self.main_session_id = main_session_id
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.title = title
        self.description = description

    def format_object(self):
        return {
            "id": self.id, 
            "type": self.type,
            "main_session_id": self.main_session_id,
            "date": self.date,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "title": self.title,
            "description": self.description
        }