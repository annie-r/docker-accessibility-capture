import socket   #for sockets
import sys  #for exit
from message import *
from node import Node

if __name__ == '__main__':
	
	network = Node(8888)
	print "sending"
	sys.stdout.flush()
	#network.send_message_to_node("serv","testing")
	sys.stdout.flush()
	network.start()
	#network.run()


# try:
#     #create an AF_INET, STREAM socket (TCP)
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# except socket.error, msg:
#     print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
#     sys.exit();
 
# print 'Socket Created'
 
# host = 'serv'
# port = 8888
 
# try:
#     remote_ip = socket.gethostbyname( host )
 
# except socket.gaierror:
#     #could not resolve
#     print 'Hostname could not be resolved. Exiting'
#     sys.exit()
     
# print 'Ip address of ' + host + ' is ' + remote_ip
 
# #Connect to remote server
# s.connect((remote_ip , port))

# print 'Socket Connected to ' + host + ' on ip ' + remote_ip
# #while 1:
# try:
# 	#request = ("1")
# 	#print("Client %d sending request to server node %d \t Request for operation: %s"  % (client_id, server_node, operation))
# 	#s.send(request)

# 	#response = s.recv(1024)

# 	#print ("response: "+response)
# 	while 1:
# 		data = "test"
# 		s.send(data)
# 		#msg = Message("cont1", SCREENSHOT, "Skype", "test.png")
# 		#s.send(msg.serializeMessage())

# 		response = s.recv(1024)
# 		print ("response: "+response)
# except KeyboardInterrupt:
# 	s.close()

