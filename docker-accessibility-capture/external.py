import socket
from message import *
from client_node import ClientNode
#have to use docker-machine ip to find ip address!!
c = ClientNode(8777, "client")
c.start()

# s = socket.socket()
# s.connect(("192.168.99.100",8888))
# print ("sending")
# msg = Message("client",WEB_SERVER_INTRO,"Skype","test.txt")
# s.sendall(msg.serializeMessage().encode())
# print ("sending")
# msg = Message("client",TRAVERSAL_DATA,"Skype","test.txt")
# s.sendall(msg.serializeMessage().encode())
# print("rec")
# resp = s.recv(2046)
# print ("resp: "+str(resp))