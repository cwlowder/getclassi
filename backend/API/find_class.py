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
	elif "q" not in query or len(query["q"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?q=%"
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
				"results": [
					{
						"crn": "1",
						"class": "cs241"
					},
					{
						"crn": "2",
						"class": "cs210"
					},
					{
						"crn": "3",
						"class": "cs233"
					}
				]
			}
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		q = query["q"][0]
		sql = "SELECT CRN, Title FROM Classes WHERE Title LIKE '%" + q + "%'"
		try:
			db.mycursor.execute(sql)
			results = [{"class":row[1],"crn":row[0]} for row in db.mycursor.fetchall()]
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				MESSAGE: {"results": results}
			})
		except:
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "oopsie I made a poopsie"
			})
	print(message)
	return [message.encode()]
def find_class(environ, start_response):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
