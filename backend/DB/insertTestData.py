import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import getpass
from CONSTANTS import *
import DB.database as db
import time
import random

def testData():
	mydb, mycursor = db.connect()
	teachers = ["Abdu", "Zilles", "Angrave", "Fleck", "Chatman"]
	classes = ["cs125", "cs126", "cs225", "cs233", "cs241", "cs411", "cs440", "tam212", "ese360", "cee330", "eng100", "aas100"]
	val = []
	sql = "INSERT INTO Users (NetId, Name) VALUES (%s, %s)"
	for user in range(0, 10):
		val += [(str(user), "Julian" + str(user))]
	mycursor.executemany(sql, val)

	val = []
	sql = "INSERT INTO Classes (CRN, Title, Department, Instructor) VALUES (%s, %s, %s, %s)"
	crn = 1000
	for c in classes:
		teacher = teachers[((crn-1000) % len(teachers))]
		val += [(str(crn), c, c[:-3], teacher)]
		crn += 1
	mycursor.executemany(sql, val)


	val = []
	sql =  "INSERT INTO Events (CRN, Title, DueDate, Event_Des) VALUES (%s, %s, %s, %s)"
	current = time.time()
	crn = 1000
	for c in classes:
		x = crn - 1000
		for assignment in range(0,5):
			val += [(str(crn), "MP" + str(assignment), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current + (10000 * x + x))), "This assignment exists")]
		crn += 1
	mycursor.executemany(sql, val)

	val = []
	sql =  "INSERT INTO Enrollments (CRN, NetId) VALUES (%s, %s)"
	for user in range(0, 10):
		# pick 4 random classes to enroll in
		for crn in random.sample(list(range(1000,1000+len(classes))), 4):
			val += [(str(crn), str(user))]
	mycursor.executemany(sql, val)
	mydb.commit()
	mydb.close()

testData()
