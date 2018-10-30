import sys
import mysql.connector
import os
sys.path.insert(0, os.path.dirname(__file__) + "/..")
import DB.database as db


def dropTables():
    sql = "DROP TABLE IF EXISTS Events"
    db.mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Enrollments"
    db.mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Users"
    db.mycursor.execute(sql)
    sql = "DROP TABLE IF EXISTS Classes"
    db.mycursor.execute(sql)




db.connect()
dropTables()
