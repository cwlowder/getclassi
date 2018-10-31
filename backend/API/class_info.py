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
	elif "crn" not in query or len(query["crn"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?crn=%"
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
				"crn": str(query["crn"][0]),
				"class": "cs241",
				"department": "cs",
				"instructor": "John Doe"
			}
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		crn = query["crn"][0]
		sql = "SELECT Title, CRN, Department, Instructor FROM Classes WHERE CRN = %s"
		mydb = None
		try:
			mydb, mycursor = db.connect()
			val = (crn,)
			mycursor.execute(sql, val)
			results = db.mycursor.fetchall()
			if len(results) == 1:
				start_response('200 OK', [('Content-Type', 'json')])
				row = results[0]
				message = json.dumps({
					STATUS: SUCCESS,
					MESSAGE: {
						"class": row[0],
						"crn": row[1],
						"department": row[2],
						"instructor": row[3]
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
def class_info(environ, start_response):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
