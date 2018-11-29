import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import DB.database as db


def createTables():
	mydb, mycursor = db.connect()
	f = open("createTableCommands.txt", "r")
	lines = f.readlines()

	for x in lines:
		print(x)
		mycursor.execute(x)
	mydb.close()

createTables()
