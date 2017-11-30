import socket   #for sockets
import sys  #for exit
 
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'
 
host = 'serv'
port = 8888
 
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
 
#Connect to remote server
s.connect((remote_ip , port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip
#while 1:
try:
	#request = ("1")
	#print("Client %d sending request to server node %d \t Request for operation: %s"  % (client_id, server_node, operation))
	#s.send(request)

	#response = s.recv(1024)

	#print ("response: "+response)
	data = "data/nowScreen.png"
	img = open(data,'r')
	while True:
		strng = img.readline(512)
		if not strng:
		    break
		s.send(strng)
	img.close()
	print "Data sent successfully"

	response = s.recv(1024)
	print ("response: "+response)
except KeyboardInterrupt:
	s.close()

