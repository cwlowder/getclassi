from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import time
import DB.database as db

from traceback import print_exc


def check_request(environ, start_response):
	query = pq(environ[QUERY])
	if environ[REQUEST_METHOD] != METHOD_GET:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting POST"
		})
	else:
		return ""

def dummy(environ, start_response):
	print("Dummy")
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		payload = {
			"1000":"cs241",
			"1000":"tp103",
			"1000":"astr120"
		}
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: payload
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response, netId):
	message = check_request(environ,start_response)
	if message == "":
		mydb = None
		sql = "SELECT Classes.CRN, Classes.Title FROM Classes INNER JOIN Enrollments ON Classes.CRN = Enrollments.CRN WHERE Enrollments.NetId = %s"
		val = (netId,)
		try:
			mydb, mycursor = db.connect()
			mycursor.execute(sql, val)
			resultsClasses = mycursor.fetchall()

			classes = {}
			for row in resultsClasses:
				classes[row[0]] = row[1]

			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				MESSAGE: classes
			})
		except:
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "Internal server error"
			})
		finally:
			if mydb:
				mydb.close()
	return [message.encode()]


def list_classes(environ, start_response, netId):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response, netId)
