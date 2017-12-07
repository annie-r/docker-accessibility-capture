import socket
import sys
from message import *

class Network:
	def __init__(self, port, cont_name):
		self.RECV_BUFFER = 4096
		self.PORT = 8888
		self.name = cont_name
		print ("created")



	# message is of type string
	# node is name of node within docker network
	def send_message_to_node(self, cont_name, port, message):
		print ("sending "+str(message)+" to "+str(cont_name))
		sys.stdout.flush()
		ip = socket.gethostbyname(cont_name)
		self.send_message((cont_name,port),message)

		

	def send_message(self, full_addr, message):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(full_addr)
		s.send(message.encode())
		s.close()

	def start(self):

		# Run the TCP serverdoc

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(),self.PORT))
		self.socket.listen(10)
		self.socket.setblocking(True)
		print ("host:" + socket.getfqdn())


		#listen for incoming connection from other docker nodes
		# TODO: figure out how to connect from outside docker network
		while True:
			print ("waiting")
			sys.stdout.flush()
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

