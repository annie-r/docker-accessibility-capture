from threading import Thread, Lock
import sys
sys.path.insert(0, '../docker') 
import client_node
import message
import networking

# Class for communicating between the web server and docker containers
class DockerCommunicator:
	def __init__(self, couch_db): 
		self.PORT = 8777
		self.name = "client"

		# Database instance to update the couchdb database from the thread
		self.db = couch_db

		# Intialize connection to the Docker containers
		print("Initializing connection to Docker containers..")
		self.docker_client = client_node.ClientNode(self.PORT, self.name)
		self.docker_client_thread = Thread(target=self.docker_client.start, args=[self.receive_docker_app_message])
		self.docker_client_thread.start()

	def send_docker_app_message(self, screenshot_id, app_name, traversal_path): 
		# Send message with the traversal path and app name to the docker master
		print("Sending traversal message to the Docker master.")
		msg = message.Message("client", message.TRAVERSAL_DATA, app_name, traversal_path)
		self.docker_client.send_message((self.docker_client.dock_master_ip, self.docker_client.dock_master_port), msg.serializeMessage())

	def receive_docker_app_message(self, app_name, screenshot_path): 
		print("Message was received by the Docker master. Creating a new creenshot record.")

		# Get message from docker & update the record
		self.db.create_new_screenshot_document(app_name, screenshot_path)


