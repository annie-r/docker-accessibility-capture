import couchdb
import os
import sys
import json
import base64
import io
from PIL import Image

# Intialize Server
couchdbserver = os.getenv("COUCHDBSERVER")
couchdbserver = couchdbserver if couchdbserver is not None else "http://127.0.0.1:5984"
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
with open('documents/test.json') as json_data: 
	test_data = json.load(json_data)
	screenshots = test_data['screenshots']
	for screenshot in screenshots: 
		image_path = screenshot["screenshot"]
		img = open(image_path, 'rb')
		img_data = img.read()
		img_b64 = base64.b64encode(img_data)
		img_b64_string = img_b64.decode("utf-8")

		screenshot["imageData"] = "data:image/png;base64, " + img_b64_string

		doc_id = db.save(screenshot)

		# # Store the attachment with the document
		# image_bytes = Image.open(image_path).tobytes()
		# db.put_attachment(doc, image_bytes, filename=image_path, content_type="image/png")∂

	apps = test_data['apps']
	for app in apps: 
		db.save(app)

# Load views
with open('documents/views.json') as json_data: 
	views_data = json.load(json_data)
	views = views_data['views']
	for view in views: 
		db.save(view)

