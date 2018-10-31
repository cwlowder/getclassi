from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import DB.database as db
from traceback import print_exc

def check_request(environ,start_response):
	query = pq(environ[QUERY])
	print(environ)
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
	elif "CONTENT_LENGTH" not in environ:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing post body in form: {'note':'xxxxxx'}"
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

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		crn = query["crn"][0]
		body = json.loads(environ[BODY].read())
		sql = "UPDATE Classes SET Note = %s WHERE CRN = %s"
		if 'note' not in body or str(type(body['note'])) != "<class 'str'>" or len(body['note']) >= 280:
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Improper request"
			})
		else:
			val = (body['note'], crn)
			try:
				mydb, mycursor = db.connect()
				db.mycursor.execute(sql, val)
				start_response('200 OK', [('Content-Type', 'json')])
				mydb.commit()
				message = json.dumps({
					STATUS: SUCCESS
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

def set_note(environ, start_response):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
