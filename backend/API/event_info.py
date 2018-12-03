from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import DB.database as db
from traceback import print_exc

def check_request(environ, start_response):
	query = pq(environ[QUERY])
	if environ[REQUEST_METHOD] != METHOD_GET:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting GET"
		})
	elif "eventId" not in query or len(query["eventId"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?eventId=#"
		})
	else:
		return ""

def dummy(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: {
				"eventId": str(query["eventId"][0]),
				"crn": "1002",
				"Title": "mp2",
				"DueDate": "11-29-2018 10:12",
				"description": "Just another annoying event"
			}
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		eventId = query["eventId"][0]
		sql = "SELECT CRN, Title, DueDate, Event_Des FROM Events WHERE EventId = %s"
		mydb = None
		try:
			mydb, mycursor = db.connect()
			val = (eventId,)
			mycursor.execute(sql, val)
			results = mycursor.fetchall()
			if len(results) == 1:
				start_response('200 OK', [('Content-Type', 'json')])
				row = results[0]
				message = json.dumps({
					STATUS: SUCCESS,
					MESSAGE: {
						"eventId": str(query["eventId"][0]),
						"crn": row[0],
						"title": row[1],
						"duedate": row[2],
						"desc": row[3]
					}
				})
			else:
				start_response('400 Bad Request', [('Content-Type', 'json')])
				message = json.dumps({
					STATUS: FAILED,
					MESSAGE: "class does not exist"
				})
		except:
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "oopsie I made a poopsie"
			})
		finally:
			if mydb:
				mydb.close()

	print(message)
	return [message.encode()]
def event_info(environ, start_response, netId):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
