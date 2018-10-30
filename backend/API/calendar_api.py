from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq

def check_request(environ, start_response):
	query = pq(environ[QUERY])
	if environ[REQUEST_METHOD] != METHOD_GET:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting POST"
		})
	elif "date" not in query or len(query["date"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?date=today"
		})
	else:
		return ""

def dummy(environ, start_response):
	print("Dummy")
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		payload = {
				"events": [
					{
						"crn": 1,
						"class": "cs241",
						"title": "MP1",
						"desc": "this assignment is harder than the teacher expected"
					},
					{
						"crn": 2,
						"class": "cs411",
						"title": "MIDTERM 1",
						"desc": "Maybe this test was too long?"
					},
					{
						"crn": 3,
						"class": "tam211",
						"title": "HW3",
						"desc": "What is in a physics?"

					}
				]
			}
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: payload
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	raise Exception('Todo implement real calander api')	

def calendar(environ, start_response):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)