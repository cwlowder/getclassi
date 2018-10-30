from CONSTANTS import *
mydb = None
mycursor = None

def init():
    mydb = mysql.connector.connect(
    	host=DB_HOST,
    	user=DB_USERNAME,
    	passwd=DB_PASSWORD,
    	database=DB_USERNAME
    )
    mycursor = mydb.cursor()

def runQuery(query):
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult
