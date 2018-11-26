from CONSTANTS import *
import json

from http.cookies import SimpleCookie
from urllib.parse import parse_qs as pq
import DB.database as db
from traceback import print_exc
from auth import stop_session

def check_request(environ, start_response):
	if environ[REQUEST_METHOD] != METHOD_POST:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting GET"
		})
	else:
		return ""

def dummy(environ, start_response):
	message = check_request(environ,start_response)
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		message = json.dumps({
			STATUS: SUCCESS,
		})
	return [message.encode()]

def real(environ, start_response):
	message = check_request(environ,start_response)
	if message == "":
		try:
			raw_cookies = environ[COOKIES]
			cookie = SimpleCookie()
			cookie.load(raw_cookies)
			sessionID = cookie['sessionID'].value
			print("SESSION:", sessionID)
			stopped = stop_session(sessionID)
			if not stopped:
				raise Exception("Did not delete cookie")
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps( {
				STATUS: SUCCESS,
			})
		except:
			print_exc()
			start_response('400 Bad Request', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Error in Database, check your code"
			})
	return [message.encode()]

def sign_out(environ, start_response, netId):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
