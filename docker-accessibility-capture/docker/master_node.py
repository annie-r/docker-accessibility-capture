from networking import Network
from message import *

class Master(Network):
	def __init__(self, port, name):
		Network.__init__(self,port,name)
		self.apps = ["Skype","Gmail"]
		self.app_to_cont = {"Skype":"emu1", "Gmail":"emu1"}
		self.web_server_address = None

	def parse_message(self, data, addr=None):
		msg = Message()
		msg.deserializeMessage(data)
		print ("addr in "+str(msg.type)+" parse:"+str(addr))
		#TODO: make different message type b/c this is just hijaking
		if msg.type == WEB_SERVER_INTRO:
			self.web_server_address = (msg.appName, int(msg.fileName))
		if msg.type == TRAVERSAL_DATA:
			#TODO: check that the file is valid and in shared directory
			# find right emu container for the app
			emu_cont = self.app_to_cont[msg.appName]
			msg.sender = self.name
			# forward the message
			self.send_message_to_node(emu_cont, self.PORT, msg.serializeMessage())
			
		elif msg.type == SCREENSHOT_READY:
			#send msg to web server
			print ("web serv addr: "+str(self.web_server_address))
			msg.sender = self.name
			self.send_message(self.web_server_address,msg.serializeMessage())

if __name__ == '__main__':
    m = Master(8888, "serv")
    m.start()