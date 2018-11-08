from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import DB.database as db
from traceback import print_exc

def check_request(environ, start_response):
	query = pq(environ[QUERY])
	if environ[REQUEST_METHOD] != METHOD_POST:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting POST"
		})
	elif "crn" not in query or len(query["crn"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?crn=%"
		})
	else:
		return ""


def dummy(environ, start_response):
	message = check_request(environ, start_response)
	query = pq(environ[QUERY])
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		message = json.dumps({
			STATUS: SUCCESS
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response, netId):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		crn = query["crn"][0]
		sql = "DELETE FROM Enrollments WHERE CRN = %s and NetId=%s"
		val = (crn, netId) #TODO CHANGE TO LOGGED IN USER
		mydb = None
		try:
			mydb, mycursor = db.connect()
			#db.mydb.start_transaction(isolation_level=SERIALIZABLE, readonly=False)
			mycursor.execute(sql, val)
			if mycursor.rowcount > 0:
				start_response('200 OK', [('Content-Type', 'json')])
				mydb.commit()
				message = json.dumps({
					STATUS: SUCCESS
				})
			else:
				start_response('400 Bad Request', [('Content-Type', 'json')])
				mydb.commit()
				message = json.dumps({
					STATUS: FAILED,
					MESSAGE: "User is not enrolled in class"
				})
		except Exception as e:
			db.mydb.rollback()
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: str(e)
			})
		finally:
			if mydb:
				mydb.close()
	print(message)
	return [message.encode()]

def drop_class(environ, start_response, netId):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response, netId)
