import sys
sys.path.insert(0, 'database')
import db_table
import pandas as pd
# sys.path.insert(0, 'model')
# from db_table import *

# from Room import Room
# from Session import Session
# from 
 

# class ImportAgenda:
#     def __init__(self):
#         return
    
#     def parsing():

agenda = pd.read_excel('./database/agenda.xls', sheet_name='Agenda', skiprows=14)
for i in agenda.index:
    print(agenda["*Date"][i], agenda["*Time Start"][i], agenda["*Time End"][i])
    