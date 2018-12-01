from CONSTANTS import *
import json
from fnmatch import fnmatch
from traceback import print_exc

from http.cookies import SimpleCookie
from auth import session_auth

from API.calendar_api import calendar
from API.drop_class import drop_class
from API.find_class import find_class
from API.add_class import add_class
from API.class_info import class_info
from API.set_note import set_note
from API.sign_in import sign_in
from API.sign_out import sign_out
from API.list_classes import list_classes
from API.mark_event import mark_event
from API.update_event import update_event
from API.event_info import event_info
from API.create_event import create_event
from API.upload_doc import upload_doc

def not_implemented(environ, start_response, netid):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = {
		STATUS: FAILED,
		MESSAGE: "This api is not implemented"
	}
	return [json.dumps(message).encode()]

def not_signedin(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/json')])
	message = {
		STATUS: FAILED,
		MESSAGE: "Invalid sessionID"
	}
	return [json.dumps(message).encode()]

def test_api(environ, start_response, netid):
	path = environ[PATH]
	query = environ[QUERY]
	start_response('200 OK', [('Content-Type', 'json')])
	message = json.dumps({
		STATUS: SUCCESS,
		MESSAGE: {
			"query": query,
			"path": path
		}
	})
	return [message.encode()]

def dev_api(environ, start_response, netid):
	if netid in ADMINS:
		start_response('200 OK', [('Content-Type', 'json')])
		return [(str(environ)).encode()]
	else:
		start_response('401 Unauthorized', [('Content-Type', 'json')])
		return ["{}".encode()]

routes = [
	('calendar', calendar),
	('drop_class',drop_class),
	('find_class',find_class),
	('add_class',add_class),
	('test_api', test_api),
	('class_info', class_info),
	('set_note', set_note),
	('sign_in', sign_in),
	('sign_out', sign_out),
	('dev_api', dev_api),
	('list_classes', list_classes),
	('mark_event', mark_event),
	('update_event', update_event),
	('event_info', event_info),
	('upload_doc', upload_doc),
	('create_event', create_event)
	('*', not_implemented)
]


def api(environ, start_response):
	req_path = environ[PATH].strip()[1:]
	print(req_path)

	netId = None
	if req_path not in ['api/sign_in']:
		try:
			raw_cookies = environ[COOKIES]
			cookie = SimpleCookie()
			cookie.load(raw_cookies)
			sessionID = cookie['sessionID'].value
			netId = session_auth(sessionID)
		except:
			return not_signedin(environ, start_response)
	try:
		for path, app in routes:
			if fnmatch(req_path, "api/" + path):
				print("Called", path)
				return app(environ, start_response, netId)
	except Exception as e:
		print("Error in api:", e)
		print_exc()
		start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Error occured on the server"
		})

	return not_implemented(environ, start_response)
