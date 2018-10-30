import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import DB.database as db


def createTables():
	f = open("createTableCommands.txt", "r")
	lines = f.readlines()

	for x in lines:
		print(x)
		db.mycursor.execute(x)
db.connect()
createTables()
