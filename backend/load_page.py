import os
import sys
from CONSTANTS import *

def not_found(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = "404 Not found"
	return [message.encode()]

def load_page(environ, start_response):
	path = "frontend" + environ[PATH]
	if path[-1] == "/":
		path += "index.html"
	
	#print("PATH:", path, "CWD:", os.getcwd())
	
	try:
		message = ""
		with open(path, "r") as file:
			for line in file.readlines():
				message += line + "\n"

		start_response('200 OK', [('Content-Type', 'text/html')])
		return [message.encode()]
	except Exception as e:
		# Error occured 
		# TODO specify 404.html file
		return not_found(environ, start_response)
