from flask import Flask, render_template, redirect, url_for, request
import couchdb
import os
import json
import yaml 
import sys
import communicator
import db
import signal

app = Flask(__name__)

couchdbserver = os.getenv("COUCHDBSERVER")
print("Server: " + couchdbserver)

couchdbname = os.getenv("COUCHDBNAME")
couchdbname = couchdbname if couchdbname is not None else "accessibility"
print("Database: " + couchdbname)

# Shared file server
fileserver = os.getenv("FILESERVER")
fileserver = fileserver if fileserver is not None else "/Users/Amanda/GitHub/docker-accessibility-capture/docker-accessibility-capture/shared_files"
print("File server: " + fileserver)

# Intializes the docker communicator to start the communication channels with the Docker master
couch_db = db.CouchDatabase(couchdbserver, couchdbname, fileserver)
docker_communicator = communicator.DockerCommunicator(couch_db)

@app.route('/')
def home():
	next_app_data = couch_db.get_next_app_data()
	if next_app_data is not None:
		screenshot_id, image_data = next_app_data
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

	text_value = ""
	if input_type == "text": 
		text_value = data["text"]

	couch_db.update_screenshot_document(screenshot_id, click_coords, input_type, text_value)
	app_name = couch_db.get_app_for_screenshot(screenshot_id)

	if app_name is not None: 
		# Write yaml file ffor traversal data
		directory = os.path.join(fileserver, "inputs")
		print("file exists " + str(os.path.exists(directory)))

		traversal_name = screenshot_id + ".yaml"
		traversal_path = os.path.join(fileserver, "inputs", traversal_name)
		write_traversal_file(traversal_path, app_name, input_type, (clientX, clientY), text_value)

		docker_communicator.send_docker_app_message(screenshot_id, app_name, traversal_name)

	# # Call the recieve message from here for now 
	# screenshot_path = os.path.join(fileserver, "images", "Home1.png") # Update file path with screenshot+id later
	# # receive_docker_app_message(app_name, screenshot_path)

	return url_for('home')

def write_traversal_file(traversal_path, app_name, input_type, user_coordinates, text=""):
	with open(traversal_path, 'w') as traversal_file: 
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

		yaml.dump(message, traversal_file)
	print("Wrote message file to: " + traversal_path)

if __name__ == '__main__':
	# Make new instance of network class 
	app.run()

