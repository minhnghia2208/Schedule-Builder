import sys
sys.path.insert(0, 'database')
sys.path.insert(0, 'model')
import pandas as pd
from constant import COLUMNS, SESSION_TYPE
from session import Session
from helper import Create_Table_Helper
 
class ImportAgenda:
    # FILE_DIR = './database/agenda.xls'
    
    def __init__(self, file_name):
        helper = Create_Table_Helper()
        self.file_name = file_name
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

    # All Database action will not be Try and Catch for Errors due to out of scope of current Task
    def parsing(self):
        def insert_to_tables(data, root_id = None):
            def insert_session():
                session = Session(
                data[0], 
                data[1][COLUMNS.SESSION_TYPE.value],
                data[1][COLUMNS.DATE.value],
                data[1][COLUMNS.STIME.value],
                data[1][COLUMNS.ETIME.value],
                data[1][COLUMNS.SESSION_TITLE.value],
                data[1][COLUMNS.DESCIPTION.value],
                root_id
                )
                try:
                    self.sessions.insert(session.format_object())
                # except NameError:
                #     print(NameError)
                except:
                    print("Error")

            def insert_room():
                # Check if Room exist in Database
                room = self.rooms.select([], { "name": data[1][COLUMNS.ROOM.value] })
                if len(room) == 0:
                    try:
                        self.rooms.insert({ "id": data[0], "name": data[1][COLUMNS.ROOM.value]})
                        self.session_room.insert({ "sessionid": data[0], "roomid": data[0]})
                    # except NameError:
                    #     print(NameError)
                    except:
                        print("Error")
                else:
                    try:
                        self.session_room.insert({ "sessionid": data[0], "roomid": room[0]["id"]})
                    # except NameError:
                    #     print(NameError)
                    except:
                        print("Error")

            def insert_speaker():
                speaker_names = [data[1][COLUMNS.SPEAKER.value]]
                if data[1][COLUMNS.SPEAKER.value]:
                    speaker_names = str(data[1][COLUMNS.SPEAKER.value]).split("; ")
                speakers_exist, speakers_not_exist = [], []

                for name in speaker_names:
                    try:
                        speaker = self.speakers.select([], { "name": name })
                        if len(speaker) > 0:
                            speakers_exist.append(speaker)
                        else:
                            speakers_not_exist.append(name)
                    except:
                        print("Error")

                # Find next speaker id
                speaker_id = self.speakers.select(["COUNT(id)"])[0]["COUNT(id)"]
                for speaker in speakers_not_exist:
                    speaker_id += 1
                    try:
                        self.speakers.insert({ "id": speaker_id, "name": speaker})
                        self.session_speaker.insert({ "sessionid": data[0], "speakerid": speaker_id})
                    except NameError:
                        print(NameError)
                    # except:
                    #     print("Error")

                for speaker in speakers_exist:
                    speaker_id += 1
                    try:
                        self.session_speaker.insert({ "sessionid": data[0], "speakerid": speaker[0]["id"]})
                    # except NameError:
                    #     print(NameError)
                    except:
                        print("Error")

            insert_session()
            insert_room()
            insert_speaker()

        agenda = pd.read_excel(self.file_name, sheet_name='Agenda', skiprows=14)

        # prev_id to store id of latest Main_Session
        # if encounter Sub_Session, assign prev_id to Session table as FOREIGN KEY
        prev_id = -1
        for i in agenda.iterrows():
            if i[1][COLUMNS.SESSION_TYPE.value] == SESSION_TYPE.MAIN.value:
                prev_id = i[0]
                insert_to_tables(i)
            else:
                insert_to_tables(i, prev_id)


def main():
    ia = ImportAgenda(sys.argv[1])
    ia.parsing()
    return

if __name__ == "__main__":
    main()