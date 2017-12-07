
from flask import Flask, render_template, redirect, url_for, request
import couchdb
import os
import random
import json
import uuid
import yaml 
import base64

app = Flask(__name__)

# Intialize Database
couchdbserver = os.getenv("COUCHDBSERVER")
couch = couchdb.Server(couchdbserver)
print("Server: " + couchdbserver)

couchdbname = os.getenv("COUCHDBNAME")
couchdbname = couchdbname if couchdbname is not None else "accessibility"
print("Database: " + couchdbname)

# Shared file server
fileserver = os.getenv("FILESERVER")
fileserver = fileserver if fileserver is not None else "/Users/Amanda/GitHub/docker-accessibility-capture/docker-accessibility-capture/shared_files"
print("File server: " + fileserver)

db = None
try: 
	db = couch[couchdbname] 
except Exception: 
	print("Database not initialized. Run setup.sh first.")

@app.route('/')
def home():
	screenshots_by_app = db.view('screenshots/screenshots_by_app', include_docs=True)
	random_screenshot = get_unprocessed_screenshot(screenshots_by_app)
	if random_screenshot is not None: 
		file_name = random_screenshot['screenshot']
		image_data = random_screenshot['imageData']
		screenshot_id = random_screenshot['_id']
		return render_template('screenshots.html', screenshots=[image_data], screenshot_id=screenshot_id)
	else:
		return render_template('screenshots.html', no_screenshots=True)

@app.route('/click', methods=['POST'])
def handle_screenshot_click(): 	
	# Parse request parameters
	data = json.loads(request.data, strict=False)
	clientX = data["x"]
	clientY = data["y"]
	screenshot_id = data["id"]
	input_type = data["type"]
	click_coords = {
		"x": clientX, 
		"y": clientY
	}

	# Update the document JSON
	screenshot_doc = db[screenshot_id]
	screenshot_doc["clickCoord"] = click_coords
	screenshot_doc["needsInput"] = False
	screenshot_doc["inputType"] = input_type

	if input_type == "text": 
		textValue = data["text"]
		screenshot_doc["textValue"] = textValue

	# Save to clouddb
	db.save(screenshot_doc)

	results = db.view("screenshots/app_for_screenshot", keys=[screenshot_id])

	app_docs = [row.value for row in results] # Should return only one app
	if len(app_docs) == 1: 
		app_doc = app_docs[0]
		app_name = app_doc["app"]
		send_docker_app_message(screenshot_id, app_name, input_type, (clientX, clientY))

	# Call the recieve message from here for now 
	screenshot_path = os.path.join(fileserver, "images", "Home1.png") # Update file path with screenshot+id later
	receive_docker_app_message(app_name, screenshot_path)

	return url_for('home')

def send_docker_app_message(screenshot_id, app_name, input_type, user_coordinates, text=""): 
	# Write yaml file for coordinates

	directory = os.path.join(fileserver, "inputs")
	print("file exists " + str(os.path.exists(directory)))


	message_path = os.path.join(fileserver, "inputs", "test.yaml")
	write_message_file(message_path, app_name, input_type, user_coordinates, text)

	# Send message 

def receive_docker_app_message(app_name, screenshot_path): 
	# Get ID for the app & update 
	results = db.view("screenshots/all_apps", keys=[app_name])
	app_ids = [row.id for row in results]
	print("receive_docker_app_message")
	if len(app_ids) == 1: 
		app_id = app_ids[0]
		print(app_id)

		# Get message from docker & update the record
		create_new_screenshot_record(app_id, screenshot_path)

def fetch_screenshot(screenshot_path): 
	# Get the screenshot from the shared drive
	img = open(screenshot_path, 'rb')
	img_data = img.read()
	img_b64 = base64.b64encode(img_data)
	img_b64_string = img_b64.decode("utf-8")

	# Delete the screenshot when done 
	# os.remove(screenshot_path)

	return "data:image/png;base64, " + img_b64_string

def write_message_file(message_path, app_name, input_type, user_coordinates, text=""):
	with open(message_path, 'w') as message_file: 
		x,y = user_coordinates
		message = {
			"traversal": {
				"id": app_name, 
				"commands": {
					"type": input_type, 
					"coords": user_coordinates
				}
			}
		}

		yaml.dump(message, message_file)

def create_new_screenshot_record(app_id, screenshot_path):
	print(create_new_screenshot_record)
	screenshot_data = fetch_screenshot(screenshot_path)

	# Create and save screenshot document
	app_doc = db[app_id]
	step_num = app_doc["currentStep"]
	step_num += 1

	screenshot_id = uuid.uuid4().hex
	screenshot_doc = {
		"_id": screenshot_id, 
		"type": "screenshot",
		"needsInput": True, 
		"screenshot": screenshot_path, 
		"imageData": screenshot_data, 
		"stepNum": step_num
	}
	db.save(screenshot_doc)

	# Update the apps link to the screenshot
	app_doc["screenshots"].append(screenshot_id)
	app_doc["currentStep"] = step_num
	db.save(app_doc)

# Seems like we should be able to make a view to return only the ones with needsInput true
# couldn't figure it out though so doing it this way for now
def get_unprocessed_screenshot(screenshots): 
	needsProcessed = []
	for result in screenshots: 
		print(result)
		screenshot_doc = result['doc']
		if screenshot_doc['needsInput']: 
			needsProcessed.append(screenshot_doc)


	# Select a random index 
	total = len(needsProcessed)
	if total > 0: 
		rand_index = random.randint(0, total-1)
		return needsProcessed[rand_index]

if __name__ == '__main__':
	# Make new instance of network class 

	# Set up thread to receive commnications & send/receive messages from Docker
	# t = Thread(target=self.)
	# t.start()

	app.run()

