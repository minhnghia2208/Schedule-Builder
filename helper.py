import sys
from tkinter.tix import COLUMN
from requests import session
from sqlalchemy import null
from db_table import db_table
sys.path.insert(0, 'database')
sys.path.insert(0, 'model')

class Create_Table_Helper:
    def create_session_table(self):
        try:
            sessions = db_table("sessions", { 
                "id": "integer PRIMARY KEY", 
                "type": "text",
                "main_session_id": "interger REFERENCES sessions",
                "title": "text", 
                "description": "text",
                "date": "date",
                "time_start": "time",
                "time_end": "time"})
        except NameError:
            print(NameError)
        return sessions

    def create_room_table(self):
        try:
            rooms = db_table("rooms", {
                "id": "integer PRIMARY KEY",
                "name": "text",
            })
        except NameError:
            print(NameError)
        return rooms

    def create_session_room_table(self):
        try:
            session_room = db_table("session_room", {
                "sessionid": "integer REFERENCES sessions",
                "roomid": "integer REFERENCES rooms"
            })
        except NameError:
            print(NameError)
        return session_room

    def create_speaker_table(self):
        try:
            speakers = db_table("speakers", {
                "id": "integer PRIMARY KEY",
                "name": "text"
            })
        except NameError:
            print(NameError)
        return speakers

    def create_session_speaker_table(self):
        try:
            session_speaker = db_table("session_speaker", {
                "sessionid": "integer REFERENCES sessions",
                "speakerid": "integer REFERENCES speakers"
            })
        except NameError:
            print(NameError)
        return session_speaker