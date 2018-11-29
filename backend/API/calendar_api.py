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
	elif "numDays" not in query or len(query["numDays"]) == 0:
		start_response('400 Bad Request', [('Content-Type', 'json')])
		return json.dumps({
			STATUS: FAILED,
			MESSAGE: "Missing query parameter ?numDays=#"
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
				"dates": [
					"2018-11-28"
				],
				"titles": {
					"0":"cs241",
					"1":"tp103",
					"2":"astr120"
				},
				"events": [{
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
				}]
			}
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
		q = db.escapeString(query["date"][0])
		numDays = int(db.escapeString(query["numDays"][0]))
		dates = []

		current = time.time()
		previous = time.strftime('%Y-%m-%d', time.localtime(current - 86400))

		if q == "today":
			dates += [time.strftime('%Y-%m-%d', time.localtime(current))]
		elif q == "tomorrow":
			dates += [time.strftime('%Y-%m-%d', time.localtime(current + 86400))]
			current = current + 86400
		elif q == "yesterday":
			dates += [time.strftime('%Y-%m-%d', time.localtime(current - 86400))]
			current = current - 86400
		else:
			try:
				print(q)
				format =  time.strptime(q, "%Y-%m-%d")
				print(format)
				current = time.mktime(format)
				print(current)
				dates += [q]
			except:
				print_exc()
				start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'json')])
				message = json.dumps({
					STATUS: FAILED,
					MESSAGE: "Date query has wrong format"
				})
				return [message.encode()]

		for x in range(numDays - 1):
			dates += [time.strftime('%Y-%m-%d', time.localtime(current + 86400))]
			current += 86400
		nextDay = time.strftime('%Y-%m-%d', time.localtime(current + 86400))
		mydb = None
		sql1 = "SELECT Enrollments.CRN, Classes.Title FROM Classes INNER JOIN Enrollments ON Classes.CRN = Enrollments.CRN WHERE Enrollments.NetId = %s"
		val1 = (netId, )
		sql2 = """
		SELECT * FROM ((SELECT Classes.CRN, `Events`.`Title`, `Events`.`DueDate`, `Events`.`Event_Des`,
		`Classes`.`Title` AS CTitle, `Events`.EventId as EventId FROM Classes LEFT JOIN `Events` ON Classes.crn = `Events`.crn) As Y
		LEFT JOIN EventDone ON EventDone.EventId = Y.EventId),
		`Enrollments` WHERE `Enrollments`.crn = Y.CRN AND `Enrollments`.NetId = %s
		"""
		# Dates is not USER generated, I made it bitch thats right. I can bring down this whole system by changing motherfucking date
		sql2 +=  "AND (Y.DueDate LIKE '" + dates[0] +"%'"
		for x in range(1, len(dates)):
			sql2 += "OR Y.DueDate LIKE '" + dates[x] +"%'"
		sql2 += ")"
		val2 = (netId, )
		try:
			if len(dates) == "0":
				raise Exception('Date is not anything')
			mydb, mycursor = db.connect()
			mycursor.execute(sql1, val1)
			resultsClasses = mycursor.fetchall()
			mycursor.execute(sql2, val2)
			resultsCalendar = mycursor.fetchall()
			titles = {}
			events = {}
			for elem in dates:
				events[elem] = {}
			print("NETID:", netId)
			for row in resultsClasses:
				if row[0] not in titles:
					titles[row[0]] = row[1]
					for elem in dates:
						events[elem][row[0]] = []
			for row in resultsCalendar:
				events[row[2].split(' ')[0]][row[0]].append({
					"crn": row[0],
					"class": row[4],
					"title": row[1],
					"desc": row[3],
					"DueDate" : row[2],
					"EventId" : row[5],
					"checked" : row[6] != None
				})

			start_response('200 OK', [('Content-Type', 'json')])
			message = json.dumps({
				STATUS: SUCCESS,
				MESSAGE: {
						  "dates": dates,
						  "prev": previous,
						  "next": nextDay,
						  "titles": titles,
						  "events" : events}
			})
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
	return [message.encode()]


def calendar(environ, start_response, netId):
	if DUMMY_MODE:
		return dummy(environ, start_response)
	else:
		return real(environ, start_response, netId)
