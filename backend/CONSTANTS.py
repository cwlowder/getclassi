import os
# FLAG for dummy data mode
# If true, use dummy data, and not database
DUMMY_MODE = False

# production branch
PROD_BRANCH = "master"

LOCAL_CLIENT_ID = "667147779945-d349v2ioe3f5kvqhhsvrcvepj8jqpqrn.apps.googleusercontent.com"
SESSION_TIMEOUT = 36000 # 10 hours in seconds

# Query environ objects
PATH = "PATH_INFO"
QUERY = "QUERY_STRING"
BODY = "wsgi.input"
COOKIES = "HTTP_COOKIE"
REQUEST_METHOD = "REQUEST_METHOD"
METHOD_GET = "GET"
METHOD_POST = "POST"

# API fields
STATUS = "status"
FAILED = False
SUCCESS = True

MESSAGE = "message"

API = "API"

DB_HOST = None
DB_PASSWORD = None
DB_USERNAME = None
DB_NAME = None
if 'HOSTNAME' in os.environ:
	#Database login Path - production
	DB_HOST = "localhost"
	DB_PASSWORD = "s,LsLC~na,nd"
	DB_USERNAME = "getclassi_robot"
	DB_NAME = "getclassi_classi"
else:
	#Database login Path - testing
	DB_HOST = "sql9.freesqldatabase.com"
	DB_PASSWORD = "UdYNAIPst9"
	DB_USERNAME = "sql9263477"
	DB_NAME = DB_USERNAME

# Isolation Levels
SERIALIZABLE = "SERIALIZABLE"

# list of admin accounts which have access to slightly more features
ADMINS = ['clowder2']
