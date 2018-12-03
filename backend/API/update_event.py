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
	"title" : "Title",
	"duedate" : "DueDate",
	"desc": "Event_Des"
}

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		body = None
		eventId = query["eventId"][0]
		try:
			body = environ[BODY].read().decode("utf-8")
			body = json.loads(body)
		except:
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Please provide valid json"
			})
			return [message.encode()]
		sql = "UPDATE Events SET"
		num_attributes = 0
		vals = []
		# Extract updated values
		for key, val in body.items():
			print(key, "=", val)
			if key not in key_map:
				num_attributes = 0
				break
			if key == "duedate":
				# must validate it is a good time
				try:
					time.strptime(val, "%m-%d-%Y %H:%M")
				except:
					print_exc()
					num_attributes = 0
					break
			if type(val) != str:
				print("Improper type! expecting string but got", type(val))
				num_attributes = 0
				break
			num_attributes += 1
			sql += " " + key_map[key] + " = %s,"
			vals.append(val)

		mydb = None
		try:
			if num_attributes == 0:
				raise Exception("Invalid body provided please use one or more of the following keys with valid values: " + str(list(key_map.keys())))
			# remove trailing comma
			sql = sql[:-1]
			sql += " WHERE EventId = %s"
			vals.append(eventId)

			mydb, mycursor = db.connect()
			mycursor.execute(sql, vals)
			mydb.commit()
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS
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
	return [message.encode()]

def update_event(environ, start_response, netId):
	if netId == None:
		raise Exception("Must be a valid user")
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
