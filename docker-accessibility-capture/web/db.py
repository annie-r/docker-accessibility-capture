import couchdb 
import random 
import uuid
import os
import base64

class CouchDatabase:
	# type: execute, 
	def __init__(self, couchdbserver, couchdbname, fileserver):
		# Intialize Database
		self.couch = couchdb.Server(couchdbserver)
		self.fileserver = fileserver
		self.db = None
		try: 
			print("database name: " + couchdbname)
			self.db = self.couch[couchdbname] 
		except Exception: 
			print("Database not initialized. Run setup.sh first.")

	def create_new_screenshot_document(self, app_name, screenshot_path):
		# Get ID for the app & update 
		results = self.db.view("screenshots/all_apps", keys=[app_name])
		app_ids = [row.id for row in results]
		if len(app_ids) == 1: 
			app_id = app_ids[0]

			# Construct the path relative to the shared file server
			screenshot_path = os.path.join(self.fileserver, "images", screenshot_path)
			screenshot_data = self.fetch_screenshot_data(screenshot_path)

			# Create and save screenshot document
			app_doc = self.db[app_id]
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
			self.db.save(screenshot_doc)

			# Update the apps link to the screenshot
			app_doc["screenshots"].append(screenshot_id)
			app_doc["currentStep"] = step_num
			self.db.save(app_doc)
		else: 
			print("No app record found for: " + app_name)

	def fetch_screenshot_data(self, screenshot_path): 
		# Get the screenshot from the shared drive
		img = open(screenshot_path, 'rb')
		img_data = img.read()
		img_b64 = base64.b64encode(img_data)
		img_b64_string = img_b64.decode("utf-8")

		# Delete the screenshot when done 
		# os.remove(screenshot_path)

		return "data:image/png;base64, " + img_b64_string

	def update_screenshot_document(self, screenshot_id, click_coords, input_type, text_value=""):
		# Update the document JSON
		screenshot_doc = self.db[screenshot_id]
		screenshot_doc["clickCoord"] = click_coords
		screenshot_doc["needsInput"] = False
		screenshot_doc["inputType"] = input_type

		if input_type == "text": 
			screenshot_doc["textValue"] = text_value

		# Save to clouddb
		self.db.save(screenshot_doc)

	def get_app_for_screenshot(self, screenshot_id): 
		results = self.db.view("screenshots/app_for_screenshot", keys=[screenshot_id])
		app_docs = [row.value for row in results] # Should return only one app
		if len(app_docs) == 1: 
			app_doc = app_docs[0]
			app_name = app_doc["app"]
			return app_name

	def get_next_app_data(self): 
		screenshots_by_app = self.db.view('screenshots/screenshots_by_app', include_docs=True)
		random_screenshot = self.get_unprocessed_screenshot(screenshots_by_app)
		if random_screenshot is not None: 
			image_data = random_screenshot['imageData']
			screenshot_id = random_screenshot['_id']
			return screenshot_id, image_data

	# Seems like we should be able to make a view to return only the ones with needsInput true
	# couldn't figure it out though so doing it this way for now
	def get_unprocessed_screenshot(self, screenshots): 
		needsProcessed = []
		for result in screenshots: 
			screenshot_doc = result['doc']
			if screenshot_doc['needsInput']: 
				needsProcessed.append(screenshot_doc)

		# Select a random index 
		total = len(needsProcessed)
		if total > 0: 
			rand_index = random.randint(0, total-1)
			return needsProcessed[rand_index]