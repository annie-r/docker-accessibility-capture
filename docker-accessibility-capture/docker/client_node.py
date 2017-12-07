from networking import Network
from message import *
import socket
import os

class ClientNode(Network):
	def __init__(self, port,name):
		Network.__init__(self,port,name)
		#docker-machine ip
		self.dock_master_ip = "192.168.99.100"
		self.dock_master_port = 8888

	def parse_message(self, data, addr=None):
		msg = Message()
		msg.deserializeMessage(data)
		print ("addr in "+str(msg.type)+" parse:"+str(addr))

	def start(self):
		# Run the TCP serverdoc

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print ("ip: "+socket.gethostname())
		self.socket.bind((socket.gethostname(),self.PORT))
		self.socket.listen(10)
		self.socket.setblocking(True)
		print ("host:" + socket.getfqdn())

		# TO get ip address of web server to docker master
		msg = Message("client", WEB_SERVER_INTRO , socket.gethostbyname(socket.gethostname()), str(self.PORT))
		self.send_message((self.dock_master_ip,self.dock_master_port),msg.serializeMessage())

		#to get things rolling
		# TODO: will end up being triggered by website
		msg = Message("client",TRAVERSAL_DATA,"Skype","test.txt")
		self.send_message((self.dock_master_ip,self.dock_master_port),msg.serializeMessage())

		#listen for incoming connection from other docker nodes
		# TODO: figure out how to connect from outside docker network
		while True:
			print ("waiting")
			conn, addr = self.socket.accept()
			print ("addr: "+str(addr))
			data = conn.recv(self.RECV_BUFFER)
			print ("receiving: " + data)
			#messages = data.split("!")
			#print("messages: "+str(messages))
			#for msg in messages:
			#	if msg:
			self.parse_message(data, addr)
			conn.close()

if __name__ == '__main__':
    c = ClientNode(8777, "client")
    #msg = Message("client",TRAVERSAL_DATA,"Skype","test.txt")
    #c.send_message_to_node(c.dock_master_ip, c.dock_master_port, msg.serializeMessage())
    c.start()