from CONSTANTS import *
import json
from fnmatch import fnmatch
from traceback import print_exc
import datetime
import subprocess

def not_implemented(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = {
		STATUS: FAILED,
		MESSAGE: "This endpoint is not implemented"
	}
	return [json.dumps(message).encode()]

def git_update(environ, start_response):
	print("ENDPOINT CALLED")
	start_response('200 OK', [('Content-Type', 'text/html')])
	message = {}
	body = environ[BODY].read().decode("utf-8")
	body = json.loads(body)
	if body['ref'] == "refs/heads/" + PROD_BRANCH:
		subprocess.call(["cd", "~/getclassi;" "sh", "update_repo.sh", PROD_BRANCH])
	else:
		subprocess.call(["echo", body['ref'], ">>", "~/update.log"])
	'''
	if len(body) > 0:
		body = json.loads(body)
		f = open(datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S.txt"), "w")
		f.write(json.dumps(body))
	'''
	# TODO update endpoint
	return [json.dumps(message).encode()]

routes = [
	('update', git_update)
]


def endpoint(environ, start_response):
	req_path = environ[PATH].strip()[1:]
	print(req_path)

	try:
		for path, app in routes:
			if fnmatch(req_path, "endpoint/" + path):
				return app(environ, start_response)
	except Exception as e:
		print("Error in endpoint:", e)
		print_exc()
		start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Error occured on the server"
		})

	return not_implemented(environ, start_response)
