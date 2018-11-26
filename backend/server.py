import os
import sys
import json
from fnmatch import fnmatch
from traceback import print_exc

sys.path.insert(0, os.path.dirname(__file__))

from ENDPOINT.endpoint import endpoint 

from API.api import api
from load_page import load_page
from CONSTANTS import *

def not_found(environ, start_response):
	print("Not Found: ", environ[PATH])
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = "404 Not found"
	return [message.encode()]

def test_page(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	message = "SUP DOOD"
	return [message.encode()]

routes = [
	('/api/*', api),
	('/test', test_page),
	('/endpoint/*', endpoint),
	('/*', load_page)
]

def application(environ, start_response):
	req_path = environ[PATH].strip().split("/")[1:]

	if environ['HTTP_HOST'] == "localhost:3000":
		# This is a development server
		pass
	else:
		# Assume this is a production server
		if 'HTTPS' not in environ or environ['HTTPS'].toLower() != 'on':
			# Redirect to https
			start_response('303 see other', [('location',  "https://" + environ['HTTP_HOST'])])
			return [b'1']

	try:
		for path, app in routes:
			if fnmatch(environ[PATH], path):
				return app(environ, start_response)
	except Exception as e:
		print("Error:", e)
		print_exc()
	return not_found(environ, start_response)
