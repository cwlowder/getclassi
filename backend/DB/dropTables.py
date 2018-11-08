import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import DB.database as db


def dropTables():
    mydb, mycursor = db.connect()
    sql = "DROP TABLE IF EXISTS Events"
    mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Enrollments"
    mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Users"
    mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Classes"
    mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Sessions"
    mycursor.execute(sql)
    mydb.close()

dropTables()
