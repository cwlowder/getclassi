from CONSTANTS import *
import json
from fnmatch import fnmatch
from traceback import print_exc

from API.calendar_api import calendar
from API.drop_class import drop_class
from API.find_class import find_class
from API.add_class import add_class

def not_implemented(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = {
		STATUS: FAILED,
		MESSAGE: "This api is not implemented"
	}
	return [json.dumps(message).encode()]

def test_api(environ, start_response):
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

routes = [
	('calendar', calendar),
	('drop_class',drop_class),
	('find_class',find_class),
	('add_class',add_class),
	('test_api', test_api),
	('*', not_implemented)
]


def api(environ, start_response):
	req_path = environ[PATH].strip()[1:]
	print(req_path)
	try:
		for path, app in routes:
			if fnmatch(req_path, "api/" + path):
				print("Called", path)
				return app(environ, start_response)
	except Exception as e:
		print("Error in api:", e)
		print_exc()

	return not_implemented(environ, start_response)
