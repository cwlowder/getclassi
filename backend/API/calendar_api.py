from CONSTANTS import *
import json
from urllib.parse import parse_qs as pq
import time

def check_request(environ, start_response):
	query = pq(environ[QUERY])
	if environ[REQUEST_METHOD] != METHOD_GET:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Bad request method: expecting POST"
		})
	elif "date" not in query or len(query["date"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?date=today"
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
				"titles": {
					"0":"cs241",
					"1":"tp103",
					"2":"astr120"
				},
				"events": {
					"0": [
						{
							"crn": 0,
							"class": "cs241",
							"title": "MP1",
							"desc": "this assignment is harder than the teacher expected"
						},
						{
							"crn": 0,
							"class": "cs241",
							"title": "QUIZ1",
							"desc": "Wow! This quiz is easy-peasy"
						},
						{
							"crn": 0,
							"class": "cs241",
							"title": "LAB1",
							"desc": "Better put on those lab coats"
						}
					],
					"1": [
						{
							"crn": 0,
							"class": "tp103",
							"title": "MP1",
							"desc": "this assignment is harder than the teacher expected"
						}
					],
					"2":[]
				}
			}
		message = json.dumps({
			STATUS: SUCCESS,
			MESSAGE: payload
		})
	print("Message:", message)
	return [message.encode()]

def real(environ, start_response):
	message = check_request(environ,start_response)
	query = pq(environ[QUERY])
	if message == "":
		q = query["date"][0]
		date = ""
		current = time.time()
		if q == "today":
			date = time.strftime('%Y-%m-%d', time.gmtime(current))
			print(date)
		elif q == "tomorrow":
			date = time.strftime('%Y-%m-%d', time.gmtime(current))
		elif q == "yesterday":
			date = time.strftime('%Y-%m-%d', time.gmtime(current))
		else:
			pass #//todo implement abstract date
		mydb = None
		sql = "SELECT * FROM Classes NATURAL JOIN Events AS x, Enrollments WHERE Enrollments.crn = x.crn AND Enrollments.NetId = '0' AND x.DueDate LIKE " + "\"" + date +"%\""
		print(sql)
		try:
			if date == "":
				raise Exception('Date is not anything')
			mydb, mycursor = db.connect()
			mycursor.execute(sql)
			results = db.mycursor.fetchall()
			print(results)
			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				MESSAGE: {"results": results}
			})
			mydb.close()
		except:
			print_exc()
			start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: FAILED,
				MESSAGE: "oopsie I made a poopsie"
			})
		finally:
			if mydb:
				mydb.close()
	print(message)
	return [message.encode()]


def calendar(environ, start_response):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response)
