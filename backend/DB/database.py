from CONSTANTS import *
import mysql.connector

def escapeString(s):
	global mydb
	return mydb.converter.escape(s)

def connect():
	mydb = mysql.connector.connect(
		host=DB_HOST,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		database=DB_NAME
	)

	mycursor = mydb.cursor()
	mycursor.execute("SHOW DATABASES")
	print("Connected to database:", mydb)
	for x in mycursor:
		print(x)
	return mydb, mycursor

def runQuery(mydb, mycursor, query):
	mycursor.execute(query)
	myresult = mycursor.fetchall()
	return myresult
