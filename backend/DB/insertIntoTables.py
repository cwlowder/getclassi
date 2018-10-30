import sys
import mysql.connector
import getpass
from CONSTANTS import *
import DB.daase as db
import time

db.init()
testData()
def testData():
	val = []
	sql = "INSERT INTO Users (NetId, Name) VALUES (%s, %s)"
	for x in range(0, 10):
		val += (str(0), "Julian" + str(0))
	mycursor.execute(sql, val)
	val = []
	sql = "INSERT INTO Classes (CRN, Title, Department, Instructor) VALUES (%s, %s, %s, %s)"
	for x in range(0, 10):
		val += (str(0), "Class" + str(0), "Departement"+str(x % 3), "Abdu")
	mycursor.execute(sql, val)

	val = []
	sql =  "INSERT INTO Events (EventId, CRN, DueDate, Event_Des) VALUES (%s, %s, %s, %s)"
	for x in range(0, 20):
	 	current = time.time()
		val += (x, str(x % 10), time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current + 12000 * x)))
	mycursor.execute(sql, val)

	val = []
	sql =  "INSERT INTO Enrollments (CRN, NetId) VALUES (%s, %s)"
	for x in range(0, 30):
	 	current = time.time()
		val += (str(x % 10), str((x/3) % 10))
	 mycursor.execute(sql, val)
