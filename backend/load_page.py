import os
import sys
from CONSTANTS import *
from traceback import print_exc
from auth import session_auth
import json
from http.cookies import SimpleCookie

def not_found(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = "404 Not found"
	return [message.encode()]

def redirect(environ, start_response, dest='/index.html'):
	start_response('303 see other', [('location', dest)])
	return [b'1']

def load_page(environ, start_response):

	if environ['HTTP_HOST'] == "localhost:3000":
		# This is a development server
		pass
	# Assume this is a production server
	if 'HTTPS' not in environ or environ['HTTPS'].lower() != 'on':
		# Redirect to https
		dest = "https://" + environ['HTTP_HOST'] + environ[PATH]
		print("dest:", dest)
		start_response('301 Moved Permanently', [('Location', dest)])
		return [b'1']#["<html><head><title>Redirecting...</title></head><script language='JavaScript'>function redirectHttpToHttps(){ var httpURL= window.location.hostname + window.location.pathname + window.location.search; var httpsURL= 'https://' + httpURL; window.location = httpsURL;}redirectHttpToHttps();</script><body></body></html>".encode()]

	path = "frontend" + environ[PATH]
	if path[-1] == "/":
		path += "index.html"

	# Only one page does not require login
	if path != "frontend/index.html":
		raw_cookies = environ[COOKIES]
		cookie = SimpleCookie()
		cookie.load(raw_cookies)
		netId = None
		try:
			netId = session_auth(cookie['sessionID'].value)
		except:
			print_exc()
		finally:
			if netId == None:
				return redirect(environ, start_response)
	try:
		contentType = []
		message = ""
		if ".png" in path:
			message = open(path, "rb").read()
			contentType = [('Content-Type', 'image/png')]
		elif ".jpg" in path:
			message = open(path, "rb").read()
			contentType = [('Content-Type', 'image/jpg')]
		elif ".css" in path:
			message = open(path, "r").read().encode()
			contentType = [('Content-Type', 'text/css')]
		else:
			message = open(path, "r").read().encode()
			contentType = [('Content-Type', 'text/html')]
		start_response('200 OK', contentType)
		return [message]
	except Exception as e:
		print_exc()
		# Error occured
		# TODO specify 404.html file
		return not_found(environ, start_response)
