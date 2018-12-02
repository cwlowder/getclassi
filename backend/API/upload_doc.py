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
	elif "format" not in query or len(query["format"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?format=%"
		})
	elif "eventId" not in query or len(query["eventId"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?eventId=%"
		})
	elif "CONTENT_LENGTH" not in environ:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing post body in form: XXXXXXXXXXX...."
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
				"id": 1
			}
		})
	return [message.encode()]

def real(environ, start_response, netId):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		content = None
		try:
			content = environ[BODY].read()
			if len(content) == 0:
				raise Exception("Please provide a non empty document")
		except:
			print_exc()
			start_response('400 Bad Request', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Error uploading document"
			})
			return [message.encode()]
		eventId = query["eventId"][0]
		form = query["format"][0]
		sql = "INSERT INTO Documents (format, content, EventId, author) VALUES (%s, %s, %s, %s)"
		val = (form, content, eventId, netId) #TODO CHANGE TO LOGIN USER
		mydb = None
		try:
			mydb, mycursor = db.connect()
			mycursor.execute(sql, val)
			_id = mycursor.lastrowid
			mydb.commit()
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				"id": _id
			})
		except Exception as e:
			mydb.rollback()
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: str(e)
			})
		finally:
			if mydb:
				mydb.close()
	return [message.encode()]

def upload_doc(environ, start_response, netId):
	if netId == None:
		raise Exception("Please log in")
	if DUMMY_MODE:
		return dummy(environ, start_response, netId)
	else:
		return real(environ, start_response, netId)
