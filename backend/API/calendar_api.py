from CONSTANTS import *
import json

def dummy(environ, start_response):
	print("Dummy")
	message = ""
	if len(environ[QUERY]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		message = json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?date=today"
		})
	else:
		start_response('200 OK', [('Content-Type', 'json')])
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: {
				"events": [
					{
						"class": "cs241",
						"event": "MP1"
					},
					{
						"class": "cs411",
						"event": "MIDTERM1"
					},
					{
						"class": "tam211",
						"event": "HW3"
					}
				]
			}
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	print("real")
	raise Exception('Todo implement real calander api')	

def calendar(environ, start_response):
	print("LOL")
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)