import couchdb
import os
import sys
import json

# Intialize Server
couchdbserver = os.getenv("COUCHDBSERVER")
couch = couchdb.Server(couchdbserver)
print("Server: " + couchdbserver)

couchdbname = os.getenv("COUCHDBNAME")
couchdbname = couchdbname if couchdbname is not None else "accessibility"
print("Database: " + couchdbname)

# Initialize or create database
db = None
try: 
	db = couch[couchdbname] 
	print("Database already initialized..")
	sys.exit(0)
except Exception: 
	db = couch.create("accessibility")

# Load dataset from file and insert documents into db
with open('test.json') as json_data: 
	test_data = json.load(json_data)
	screenshots = test_data['screenshots']
	for screenshot in screenshots: 
		image_path = screenshot["screenshot"]
		image_file = open(image_path, "r")

		doc_id = db.save(screenshot)
		doc = db[doc_id[0]]

		# Store the attachment with the document
		db.put_attachment(doc, image_path, filename=image_path)

	apps = test_data['apps']
	for app in apps: 
		db.save(app)

