import sys
import mysql.connector
import getpass
from CONSTANTS import *

mydb = mysql.connector.connect(
	host=DB_HOST,
	user=DB_USERNAME,
	passwd=DB_PASSWORD,
	database=DB_USERNAME
)
mycursor = mydb.cursor()

f = open("createTableCommands.txt", "r")
mycursor = mydb.cursor()
lines = f.readlines()

for x in lines:
	print(x)
	mycursor.execute(x)
