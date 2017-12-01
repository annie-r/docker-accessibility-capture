
from flask import Flask, render_template, redirect, url_for, request
import couchdb
import os
import random
import json

app = Flask(__name__)

# Intialize Database
couchdbserver = os.getenv("COUCHDBSERVER")
couch = couchdb.Server(couchdbserver)
print("Server: " + couchdbserver)

couchdbname = os.getenv("COUCHDBNAME")
couchdbname = couchdbname if couchdbname is not None else "accessibility"
print("Database: " + couchdbname)

db = None
try: 
	db = couch[couchdbname] 
except Exception: 
	print("Database not initialized. Run setup.sh first.")

@app.route('/')
def home():
	screenshots_by_app = db.view('screenshots/screenshots_by_app', include_docs=True)
	random_screenshot = get_needs_input(screenshots_by_app)
	if random_screenshot is not None: 
		file_name = random_screenshot['screenshot']
		image_data = random_screenshot['image_data']
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

	# Update the document JSON
	screenshot_doc = db[screenshot_id]
	screenshot_doc["clickCoord"] = {
		"x": clientX, 
		"y": clientY
	}

	screenshot_doc["needsInput"] = False
	screenshot_doc["inputType"] = "click" # Assume click for now

	# Save to clouddb
	db.save(screenshot_doc)

	return url_for('home')

# Seems like we should be able to make a view to return only the ones with needsInput true
# couldn't figure it out though so doing it this way for now
def get_needs_input(screenshots_by_app): 
	needsProcessed = []
	for result in screenshots_by_app: 
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
    app.run()