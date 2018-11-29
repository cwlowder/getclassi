from CONSTANTS import *
import mysql.connector

def escapeString(s):
	mydb,_ = connect()
	mydb.close()
	return mydb.converter.escape(s)

def connect():
	mydb = mysql.connector.connect(
		host=DB_HOST,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		database=DB_NAME
	)

	mycursor = mydb.cursor()
	return mydb, mycursor

def runQuery(mydb, mycursor, query):
	mycursor.execute(query)
	myresult = mycursor.fetchall()
	return myresult
