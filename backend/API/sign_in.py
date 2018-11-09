from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import DB.database as db
from traceback import print_exc
from auth import google_auth, generate_Session, add_user

def check_request(environ, start_response):
	if environ[REQUEST_METHOD] != METHOD_POST:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting POST"
		})
	else:
		return ""

def dummy(environ, start_response):
	message = check_request(environ,start_response)
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: "69XD" * (190 // 4)
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		body = environ[BODY].read().decode("utf-8")
		body = json.loads(body)
		if 'google_token' not in body:
			start_response('400 Bad Request', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Improper request no google_token in body"
			})
		else:
			token = body['google_token']
			idinfo = google_auth(token)
			if idinfo is None:
				start_response('400 Bad Request', [('Content-Type', 'json')])
				message = json.dumps({
					STATUS: FAILED,
					MESSAGE: "Not valid google token"
				})
			else:
				try:
					netId = idinfo['email'][0].split("@")[0]
					add_user(netId)
					session = generate_Session(netId)
					start_response('200 OK', [('Content-Type', 'json')])
					message = json.dumps( {
						STATUS: SUCCESS,
						MESSAGE: session
					})
				except:
					print_exc()
					start_response('400 Bad Request', [('Content-Type', 'json')])
					message = json.dumps({
						STATUS: FAILED,
						MESSAGE: "Error in Database, check your code"
					})
	print(message)
	return [message.encode()]

def sign_in(environ, start_response, netId):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
