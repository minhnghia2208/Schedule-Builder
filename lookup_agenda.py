import sys
sys.path.insert(0, 'database')
sys.path.insert(0, 'model')
from constant import COLUMNS, SESSION_TYPE, QUERY
from helper import Create_Table_Helper

class LookupAgenda:
    def __init__(self, column, value):
        helper = Create_Table_Helper()
        self.column = column
        self.value = value
        self.sessions = helper.create_session_table()
        self.rooms = helper.create_room_table()
        self.session_room = helper.create_session_room_table()
        self.speakers = helper.create_speaker_table()
        self.session_speaker = helper.create_session_speaker_table()

    def __delete__(self):
        self.sessions.close()
        self.rooms.close()
        self.session_room.close()
        self.speakers.close()
        self.session_speaker.close()
    
    def to_string(self):
        def join_rootsession(sessions):
            for session in sessions:
                if session["type"] == SESSION_TYPE.SUB.value:
                    sessions += self.sessions.select([], { "id": session["main_session_id"] })

        def session_join_helper(sessions):
            join_rootsession(sessions)
            for session in sessions:
                speakers, rooms = [], []
                session_speakers = self.session_speaker.select([], { "sessionid": session["id"] })
                for id in session_speakers:
                    store = self.speakers.select([], { "id": id["speakerid"] })
                    if len(store) > 0:
                        speakers.append(store[0]["name"])
                
                session_rooms = self.session_room.select([], { "sessionid": session["id"] })
                for id in session_rooms:
                    store = self.rooms.select([], { "id": id["roomid"] })
                    if len(store) > 0:
                        rooms.append(store[0]["name"])
                
                print(
                    session["date"], '\t', session["time_start"], '\t', session["time_end"], '\t', 
                    session["title"], '\t', session["type"], '\t', session["description"], '\t', 
                    ", ".join(speakers), '\t', ", ".join(rooms)
                    )

        def room_join_helper(room):
            sessions_ids = self.session_room.select([], { "roomid": room[0]["id"] })
            sessions = []
            for id in sessions_ids:
                store = self.sessions.select([], { "id": id["sessionid"] })
                if len(store) > 0:
                    sessions.append(store[0])
            session_join_helper(sessions)
        
        def speaker_join_helper(speaker):
            sessions_ids = self.session_speaker.select([], { "speakerid": speaker[0]["id"] })
            sessions = []
            for id in sessions_ids:
                store = self.sessions.select([], { "id": id["sessionid"] })
                if len(store) > 0:
                    sessions.append(store[0])
            session_join_helper(sessions)
                
        
        if self.column == QUERY.DESCRIPTION.value:
            sessions = self.sessions.select([], { QUERY.DESCRIPTION.value: self.value })
            session_join_helper(sessions)

        elif self.column == QUERY.TITLE.value:
            sessions = self.sessions.select([], { QUERY.TITLE.value: self.value })
            session_join_helper(sessions)

        elif self.column == QUERY.ETIME.value:
            sessions = self.sessions.select([], { QUERY.ETIME.value: self.value })
            session_join_helper(sessions)

        elif self.column == QUERY.STIME.value:
            sessions = self.sessions.select([], { QUERY.STIME.value: self.value })
            session_join_helper(sessions)

        elif self.column == QUERY.LOCATION.value:
            room = self.rooms.select([], { "name": self.value })
            room_join_helper(room)

        elif self.column == QUERY.SPEAKER.value:
            speaker = self.speakers.select([], { "name": self.value })
            speaker_join_helper(speaker)

def main():
    la = LookupAgenda(sys.argv[1], sys.argv[2])
    la.to_string()

if __name__ == "__main__":
    main()