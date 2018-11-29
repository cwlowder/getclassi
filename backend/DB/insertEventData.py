import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import getpass
from CONSTANTS import *
import DB.database as db
import time
import random


teachers = ["Abdu", "Zilles", "Angrave", "Fleck", "Chatman"]
classes = ["cs125", "cs126", "cs225", "cs233", "cs241", "cs411", "cs440", "tam212", "ese360", "cee330", "eng100", "aas100"]

def insertEventData(day):
    mydb, mycursor = db.connect()
    val = []
    sql =  "INSERT INTO Events (CRN, Title, DueDate, Event_Des) VALUES (%s, %s, %s, %s)"
    crn = 1000
    for c in classes:
    	x = crn - 1000
    	for assignment in range(0,1 + random.randint(0,5)):
    		val += [(str(crn), "MP" + str(assignment), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(day + (100000 * (x + 1)))), "This assignment exists")]
    	crn += 1
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()

current = time.time()
for x in range(5):
    insertEventData(current + x * 86400)
    print("inserted my ass")
