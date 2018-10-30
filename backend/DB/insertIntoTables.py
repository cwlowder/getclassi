import sys
import mysql.connector
import getpass
from CONSTANTS import *
import DB.database as db

db.init()

def testData():
	val = []
	sql = "INSERT INTO Users (NetId, Name) VALUES (%s, %s)"
    for x in range(0, 10):
        val = (str(0), "Julian" + str(0))
    mycursor.execute(sql, val)

    val = []
    sql = "INSERT INTO Classes (CRN, Title, Department, Instructor) VALUES (%s, %s)"
    for x in range(0, 10):
        val = (str(0), "Class" + str(0), "Departement"+str(x % 3), "Abdu")
    mycursor.execute(sql, val)

    sql =  "INSERT INTO Events (EventId, CRN, DueDate, Event_Des) VALUES (%s, %s)"
    for x in range(0, 20):
        val
