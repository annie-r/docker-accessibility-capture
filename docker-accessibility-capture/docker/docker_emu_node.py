from networking import Network
from message import *
import os
import shutil
import sys

class EmuNode(Network):
	def __init__(self, port, name, shared_path = "./shared/"):
		Network.__init__(self,port,name)
		self.shared_path = shared_path
		self.ss_path = "./screenshots/"
		self.ss_counter = { "Gmail":1, "Skype":1}

	def parse_message(self, data, addr=None):
		msg = Message()
		msg.deserializeMessage(data)
		# from server
		print("parse_message: " + str(msg.type) + " " + msg.appName + " " + msg.fileName)
		sys.stdout.flush()
		if msg.type == TRAVERSAL_DATA:
			# TODO retrieve data
			print("parse traversal data")
			sys.stdout.flush()

			self.parse_traversal(msg.fileName)
			# act on it
			# return screenshot if there's still one to send
			ss_file = self.take_screenshot(msg.appName)

			# send message once screenshot is ready, if there is one
			# if we're out of screenshots, ignore
			if(ss_file != None):
				print("Send message to node")
				sys.stdout.flush()

				resp_msg = Message(self.name,SCREENSHOT_READY,msg.appName,ss_file)
				self.send_message_to_node("serv", self.PORT, resp_msg.serializeMessage())
			else: 
				print("Screenshot file not found")
				sys.stdout.flush()

	def parse_traversal(self, filename):
		# parse the file and extract the traversal step
		# apply to appropriate app
		# remove file
		print ("removing "+self.shared_path+"inputs/"+filename)
		sys.stdout.flush()

		os.remove(self.shared_path+"inputs/"+filename)

	# take screenshot of running emulator and store it in the shared dir

	def take_screenshot(self, app):
		# for proj, take image from set of screenshot and move to shared folder
		print("Taking screenshot of " + app)
		sys.stdout.flush()


		filename = app+str(self.ss_counter[app])+".jpg"
		filepath = self.ss_path+filename
		print ("filename: "+filename)
		sys.stdout.flush()

		if (os.path.isfile(filepath)):
			print ("moving : " +filepath + "to"+ self.shared_path+"images/"+filename)
			sys.stdout.flush()

			# shutil.move(self.ss_path+filename,self.shared_path+"images/"+filename) # Temporarily changing to a copy so we dont have to keep copying the file

			shutil.copy(self.ss_path+filename,self.shared_path+"images/"+filename)
			self.ss_counter[app] = self.ss_counter[app]+1
			return filename
		#if run out of SS for that app
		else:
			print ("No file: "+filename)
			sys.stdout.flush()

			return None

if __name__ == '__main__':
    n = EmuNode(8888, "emu1")
    n.start()