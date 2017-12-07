from networking import Network
from message import *
import os

class EmuNode(Network):
	def __init__(self, port, name, db_path = "./db/"):
		Network.__init__(self,port,name)
		self.db_path = db_path
		self.ss_path = "./screenshot/"

	def parse_message(self, data, addr=None):
		msg = Message()
		msg.deserializeMessage(data)
		# from server
		if msg.type == TRAVERSAL_DATA:
			# TODO retrieve data
			#self.parse_traversal(msg.fileName)
			#ss_file = self.take_screenshot()
			# act on it
			# return screenshot
			resp_msg = Message(self.name,SCREENSHOT_READY,"Skype","test")
			self.send_message_to_node("serv", self.PORT, resp_msg.serializeMessage())
			# forward the message


	def parse_traversal(self, filename):
		# parse the file and extract the traversal step
		# apply to appropriate app
		# remove file
		os.remove(filename)

	# take screenshot of running emulator and store it in the shared dir

	def take_screenshot(self, app):
		# for proj, take image from set of screenshot and move to shared folder
		os.rename(self.ss_file+"")

if __name__ == '__main__':
    n = EmuNode(8888, "emu1")
    n.start()