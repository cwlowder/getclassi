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
							"crn": "0",
							"class": "cs241",
							"title": "MP1",
							"desc": "this assignment is harder than the teacher expected"
						},
						{
							"crn": "0",
							"class": "cs241",
							"title": "QUIZ1",
							"desc": "Wow! This quiz is easy-peasy"
						},
						{
							"crn": "0",
							"class": "cs241",
							"title": "LAB1",
							"desc": "Better put on those lab coats"
						}
					],
					"1": [
						{
							"crn": "1",
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
		q = db.escapeString(query["date"][0])
		date = ""
		current = time.time()
		if q == "today":
			date = time.strftime('%Y-%m-%d', time.localtime(current))
			print(date)
		elif q == "tomorrow":
			date = time.strftime('%Y-%m-%d', time.localtime(current + 86400))
		elif q == "yesterday":
			date = time.strftime('%Y-%m-%d', time.localtime(current - 86400))
		else:
			pass #//todo implement abstract date
		mydb = None
		sql1 = "SELECT Enrollments.CRN, Classes.Title FROM Classes INNER JOIN Enrollments ON Classes.CRN = Enrollments.CRN WHERE Enrollments.NetId = %s"
		val1 = ("0",)
		sql2 = "SELECT * FROM (SELECT Classes.CRN, `Events`.`Title`, `Events`.`DueDate`, `Events`.`Event_Des`, `Classes`.`Title` AS CTitle FROM Classes LEFT JOIN `Events` ON Classes.crn = `Events`.crn) AS x, `Enrollments` WHERE `Enrollments`.crn = x.crn AND `Enrollments`.NetId = %s  AND x.DueDate LIKE '" + date +"%' "
		val2 = ("0",)
		try:
			if date == "":
				raise Exception('Date is not anything')
			mydb, mycursor = db.connect()
			mycursor.execute(sql1, val1)
			resultsClasses = db.mycursor.fetchall()
			mycursor.execute(sql2, val2)
			resultsCalendar = db.mycursor.fetchall()
			titles = {}
			events = {}
			for row in resultsClasses:
				if row[0] not in titles:
					titles[row[0]] = row[1]
					events[row[0]] = []
			for row in resultsCalendar:
				events[row[0]].append({
					"crn": row[0],
					"class": row[4],
					"title": row[1],
					"desc": row[3],
					"DueDate" : row[2]
				})

			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				MESSAGE: {"titles": titles,
						  "events" : events}
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
