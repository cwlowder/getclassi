import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import getpass
from CONSTANTS import *
import DB.database as db
import time



db.connect()

def testData():
	val = []
	sql = "INSERT INTO Users (NetId, Name) VALUES (%s, %s)"
	for x in range(0, 10):
		val += [(str(x), "Julian" + str(x))]
	db.mycursor.executemany(sql, val)

	val = []
	sql = "INSERT INTO Classes (CRN, Title, Department, Instructor) VALUES (%s, %s, %s, %s)"
	for x in range(0, 10):
		val += [(str(x), "Class" + str(x), "Departement"+str(x % 3), "Abdu")]
	db.mycursor.executemany(sql, val)

	val = []
	sql =  "INSERT INTO Events (EventId, CRN, Title, DueDate, Event_Des) VALUES (%s, %s, %s, %s, %s)"
	current = time.time()
	for x in range(0, 50):
		val += [(x, str(x % 10), "MP" + str(x), time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current + 6000 * x)), "EventId is that " + str(x))]
	db.mycursor.executemany(sql, val)

	val = []
	sql =  "INSERT INTO Enrollments (CRN, NetId) VALUES (%s, %s)"
	for x in range(0, 30):
		val += [(str(x % 10), str(int(x/3) % 10))]
	db.mycursor.executemany(sql, val)
	db.mydb.commit()

testData()
