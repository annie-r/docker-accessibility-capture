from networking import Network
from message import *
import os

class EmuNode(Network):
	def __init__(self, port, name, shared_path = "./shared/"):
		Network.__init__(self,port,name)
		self.shared_path = shared_path
		self.ss_path = "./screenshots/"
		self.ss_counter = { "Gmail":11}

	def parse_message(self, data, addr=None):
		msg = Message()
		msg.deserializeMessage(data)
		# from server
		if msg.type == TRAVERSAL_DATA:
			# TODO retrieve data
			self.parse_traversal(msg.fileName)
			ss_file = self.take_screenshot(msg.appName)
			# act on it
			# return screenshot if there's still one to send
			# else, ignore
			if(ss_counter(msg.app) > 0):
				resp_msg = Message(self.name,SCREENSHOT_READY,msg.appName,ss_file)
				self.send_message_to_node("serv", self.PORT, resp_msg.serializeMessage())

	def parse_traversal(self, filename):
		# parse the file and extract the traversal step
		# apply to appropriate app
		# remove file
		print ("removing "+self.shared_path+"inputs/"+filename)
		os.remove(self.shared_path+"inputs/"+filename)

	# take screenshot of running emulator and store it in the shared dir

	def take_screenshot(self, app):
		# for proj, take image from set of screenshot and move to shared folder
		filename = app+str(self.ss_counter[app])
		print ("moving : " +self.ss_path+filename + "to"+ self.shared_path+"images/"+filename)
		os.rename(self.ss_path+filename,self.shared_path+"images/"+filename)
		self.ss_counter[app] = self.ss_counter[app]-1
		return filename

if __name__ == '__main__':
    n = EmuNode(8888, "emu1")
    n.start()