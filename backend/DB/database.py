from CONSTANTS import *
import mysql

mydb = None
mycursor = None

def connect():
    global mydb
    global mycursor
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

def runQuery(query):
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult
