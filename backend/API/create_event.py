from CONSTANTS import *
import json, time
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
	elif "CONTENT_LENGTH" not in environ:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing post body in form: {'desc':'xxxxxx', 'duedate': 'xxxx-xx-xx'...}"
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

key_map = {
	"CRN" : "CRN",
	"title" : "Title",
	"duedate" : "DueDate",
	"desc": "Event_Des"
}

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		body = None
		try:
			body = environ[BODY].read().decode("utf-8")
			print(body)
			body = json.loads(body)
			sql = "INSERT INTO Events ( CRN , Title, DueDate, Event_Des) VALUES (%s, %s, %s, %s)"
			num_attributes = 0
			vals = []
			vals.append(body["CRN"])
			vals.append(body["title"])
			# Extract updated values
			try:
				time.strptime(body["duedate"], "%m-%d-%Y %H:%M")
			except:
				print_exc()
				start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
				message = json.dumps({
					STATUS: FAILED,
					MESSAGE: "Incorrect Date in duedate put it in %Y-%m-%d %H:%M:%S"
				})
				return [message.encode()]

			vals.append(body["duedate"])
			vals.append(body["desc"])
		except:
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Please provide valid json"
			})
			return [message.encode()]
		mydb = None
		try:
			print(vals)
			mydb, mycursor = db.connect()
			mycursor.execute(sql, vals)
			mydb.commit()
			_id = mycursor.lastrowid
			print("done")
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				"EventId" : _id
			})
		except Exception as e:
			if mydb is not None:
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
	print(message)
	return [message.encode()]

def create_event(environ, start_response, netId):
	if netId == None:
		raise Exception("Must be a valid user")
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
