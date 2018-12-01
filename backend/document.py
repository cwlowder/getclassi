import os
import sys
from CONSTANTS import *
from traceback import print_exc
from auth import session_auth
import DB.database as db
import json
from http.cookies import SimpleCookie

def not_found(environ, start_response):
	start_response('404 Not Found', [('Content-Type', 'text/html')])
	message = "Image not found"
	return [message.encode()]

def internal_error(environ, start_response):
	start_response('501 Internal Server Error', [('Content-Type', 'text/html')])
	message = "Please try again later"
	return [message.encode()]

def please_login(environ, start_response):
	start_response('401 Unauthorized', [('Content-Type', 'text/html')])
	message = "Please log in"
	return [message.encode()]

def load_doc(environ, start_response):
	doc_id = environ[PATH].split("/doc/")[1]

	# Check cookies
	cookie = None
	netId = None
	if COOKIES in environ:
		raw_cookies = environ[COOKIES]
		cookie = SimpleCookie()
		cookie.load(raw_cookies)
	try:
		netId = session_auth(cookie['sessionID'].value)
	except:
		return please_login(environ, start_response)
	
	form = None
	content = b''

	mydb = None
	try:
		sql = "SELECT format, content FROM Documents WHERE id = %s"
		vals = (doc_id,)
		mydb, mycursor = db.connect()
		mycursor.execute(sql, vals)
		row = mycursor.fetchall()[0]

		form = row[0]
		content = row[1]
		if mydb:
			mydb.close()
	except IndexError:
		if mydb:
			mydb.close()
		return not_found(environ, start_response)
	except:
		print_exc()
		if mydb:
			mydb.close()
		return internal_error(environ, start_response)

	try:
		contentType = []
		if form == "png":
			contentType = [('Content-Type', 'image/png')]
		elif form == "jpg":
			contentType = [('Content-Type', 'image/jpg')]
		elif form == "pdf":
			contentType = [('Content-Type', 'application/pdf')]
		elif form == "txt":
			contentType = [('Content-Type', 'text/plain')]
		else:
			return internal_error(environ, start_response)
		start_response('200 OK', contentType + [('Cache-Control', 'no-store, must-revalidate'), ('Pragma', 'no-cache'), ('Expires', '0')])
		return [content]
	except Exception as e:
		print_exc()
		return not_found(environ, start_response)
