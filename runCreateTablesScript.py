import sys
import mysql.connector
import getpass

if len(sys.argv) < 3:
	print("Please give file name and database name")
	print(python runCreateTableScript.py [File Name] [Database Name]
	exit()
f = open(sys.argv[1], "r")
print(sys.argv[2])
userName = input('UserName: ') 
password = input('Password: ')
mydb = mysql.connector.connect(
	host="localhost",
	user=userName,
	passwd=password,
	database=sys.argv[2]
)

mycursor = mydb.cursor()
lines = f.readlines()

for x in lines:
	print(x)
	mycursor.execute(x)
