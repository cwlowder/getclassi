from CONSTANTS import *
import json
from fnmatch import fnmatch
from traceback import print_exc
from google.oauth2 import id_token
from google.auth.transport import requests
import DB.database as db
import time
import secrets



def google_auth(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), LOCAL_CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        print_exc()
        print("Failed to validate id token")
        return False
        pass
    return True

def session_auth(sessionID):
    sql = "SELECT * FROM Sessions WHERE SessionToken = %s"
    val = (sessionID, ); #TODO CHANGE TO LOGIN USER
    mydb, mycursor = db.connect()
    mycursor.execute(sql, val)
    results =  mycursor.fetchall()
    mydb.close()
    if len(results) == 0:
        return None
    time = results[0][2];
    currentTime = time.time()
    if currentTime - time > SessionToken:
        mydb, mycursor = db.connect()
        sql = "DELETE FROM Sessions WHERE SessionToken = %s"
        mycursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return None
    return results[0][0]

def generate_Session(netId):
    session = secrets.token_urlsafe(190)
    sql = "SELECT * FROM Sessions WHERE SessionToken = %s"
    val = (session, ); #TODO CHANGE TO LOGIN USER
    mydb, mycursor = db.connect()
    mycursor.execute(sql, val)
    results =  mycursor.fetchall()
    mydb.close()
    if len(results) == 0:
        mydb, mycursor = db.connect()
        sql = "INSERT INTO Sessions (NetId, SessionToken, CreateTime)  VALUES (%s, %s, %s)"
        val = (netId, session, time.time());
        mydb, mycursor = db.connect()
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return session
    else:
        generate_Session()

def add_user(netId, name = "Abdu"):
    sql = "SELECT * FROM Users WHERE NetId = %s"
    val = (netId, ); #TODO CHANGE TO LOGIN USER
    mydb, mycursor = db.connect()
    mycursor.execute(sql, val)
    results =  mycursor.fetchall()
    mydb.close()
    if len(results) == 0:
        mydb, mycursor = db.connect()
        sql = "INSERT INTO Users (NetId, Name)  VALUES (%s, %s)"
        val = (netId, name);
        mydb, mycursor = db.connect()
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return True
    else:
        return False
