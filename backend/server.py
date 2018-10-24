import os
import sys
import json
from fnmatch import fnmatch

sys.path.insert(0, os.path.dirname(__file__))

PATH = "PATH_INFO"
QUERY = "QUERY_STRING"
API = "API"

def not_found(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = "404 Not found"
	return [message.encode()]

def test_page(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	message = "SUP DOOD"
	return [message.encode()]

def load_page(environ, start_response):
	path = "frontend" + environ[PATH]
	if path[-1] == "/":
		path += "index.html"
	print("PATH:", path, "CWD:", os.getcwd())
	try:
		message = ""
		with open(path, "r") as file:
			for line in file.readlines():
				message += line + "\n"
		print(message)

		start_response('200 OK', [('Content-Type', 'text/html')])
		return [message.encode()]
	except Exception as e:
		print(e)
		return not_found(environ, start_response)

def api(environ, start_response):
	path = environ[PATH]
	query = environ[QUERY]
	start_response('200 OK', [('Content-Type', 'json')])
	message = json.dumps({
		"test":"LOL",
		"query": query,
		"path": path
	})
	print(">>", message)
	return [message.encode()]

routes = [
	('/api/*', api),
	('/test', test_page),
	('/*', load_page)
]

def application(environ, start_response):
	print("Requested:", )

	req_path = environ[PATH].strip().split("/")[1:]

	for path, app in routes:
		if fnmatch(environ[PATH], path):
			return app(environ, start_response)
	return not_found(environ, start_response)