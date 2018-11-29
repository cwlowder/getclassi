from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import DB.database as db
from traceback import print_exc

def check_request(environ,start_response):
	query = pq(environ[QUERY])
	if environ[REQUEST_METHOD] != METHOD_POST:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting POST"
		})
	elif "EventId" not in query or len(query["EventId"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?EventId=#"
		})
	elif "check" not in query or len(query["check"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?check=#"
		})
	else:
		return ""

def dummy(environ, start_response):
	message = check_request(environ,start_response)
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
		EventId = query["EventId"][0]
		check = query["check"][0].lower() == "true"
		sql = ""
		val = (EventId, netId )
		if check:
			sql = "INSERT INTO EventDone (EventId, NetId) VALUES (%s, %s)"
		else:
			sql = "DELETE FROM EventDone WHERE EventId = %s and NetId=%s"
		try:
			mydb, mycursor = db.connect()
			#db.mydb.start_transaction(isolation_level=SERIALIZABLE, readonly=False)
			mycursor.execute(sql, val)
			count = mycursor.rowcount
			start_response('200 OK', [('Content-Type', 'json')])
			mydb.commit()
			message = json.dumps({
				STATUS: SUCCESS if count == 1 else FAILED
			})
		except Exception as e:
			mydb.rollback()
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Already checked done on event" if check else "Event is already unchecked"
			})
		finally:
			if mydb:
				mydb.close()
	print(message)
	return [message.encode()]

def mark_event(environ, start_response, netId):
	if netId == None:
		raise Exception("Not logged in")
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response, netId)
