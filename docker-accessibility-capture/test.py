import socket   #for sockets
import sys  #for exit
from message import *
from networking import Network

if __name__ == '__main__':
	
	network = Network(8888)
	print "sending"
	sys.stdout.flush()
	msg = Message("test1", TRAVERSAL_DATA, "Skype", "test.png")
# 		#s.send(msg.serializeMessage())
	network.send_message_to_node("serv",msg.serializeMessage())
	#network.send_message_to_node("cont1","other test")