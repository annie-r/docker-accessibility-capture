#defines a message sent between docker emu containers and docker master container

#Message Types
INSTALL = 0
EXECUTE = 1
SCREENSHOT_TO_DB = 2
SCREENSHOT_READY = 3
WEB_DATA_TO_DB = 4
TRAVERSAL_DATA = 5
WEB_SERVER_INTRO = 6

## TODO CLEAR INPUT FILE

class Message:
	# type: execute, 
	def __init__(self, senderArg=None, typeArg=None, appNameArg=None, locationArg=None):
		self.sender = senderArg
		self.type = typeArg
		self.appName = appNameArg
		self.fileName = locationArg

	def serializeMessage(self):
		return ("SENDER="+self.sender+";TYPE="+str(self.type)+";APP="+self.appName+";FILE="+self.fileName)

	def deserializeMessage(self, stringMsg):
		components = stringMsg.split(";")
		for c in components:
			comp = c.split("=")
			if(comp[0] == "SENDER"):
				self.sender = comp[1]
			elif comp[0] == "TYPE":
				self.type = int(comp[1])
			elif comp[0] == "APP":
				self.appName = comp[1]
			elif comp[0] == "FILE":
				self.fileName = comp[1]
		if (self.type == None or self.sender == None or self.appName == None or self.fileName == None):
			print ("ERROR, incomplete message!"+stringMsg)
