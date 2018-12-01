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
	elif "eventId" not in query or len(query["eventId"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?eventId=#"
		})
	else:
		return ""

def dummy(environ, start_response):
	print("Dummy")
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		start_response('200 OK', [('Content-Type', 'json')])
		payload = [
			{
				"id": 1,
				"format": "png",
				"author": "alb2",
			},
			{
				"id": 5,
				"format": "jpg",
				"author": "mac_is_kewl",
			}
		]
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: payload
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response, netId):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		mydb = None
		eventId = query["eventId"][0]
		sql = "SELECT id, format, author FROM Documents WHERE EventId = %s"
		try:
			eventId = int(eventId)
			val = (eventId,)
			mydb, mycursor = db.connect()
			mycursor.execute(sql, val)
			results = mycursor.fetchall()

			docs = []
			for row in results:
				docs.append({
					"id": int(row[0]),
					"format": row[1],
					"author": row[2]
				})

			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				MESSAGE: docs
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


def list_docs(environ, start_response, netId):
	if netId == None:
		raise Exception("Please log in")
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response, netId)
