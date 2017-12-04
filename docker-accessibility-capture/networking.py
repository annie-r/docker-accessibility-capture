import socket
import sys
from message import *

class Network:
	def __init__(self, port):
		self.RECV_BUFFER = 4096
		self.PORT = 8874
		print ("created")

	# message is of type Message
	# node is name of node within docker network
	def send_message_to_node(self, node, message):
		print ("in send")
		sys.stdout.flush()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ip = socket.gethostbyname(node)

		s.connect((ip,self.PORT))
		s.send(message)

		s.close()

	def parse_message(self, data):
		msg = Message()
		msg.deserializeMessage(data)
		# traversal data from web server -> main docker
		# must forward to correct emu container
		# traversal data from main docker -> emu container
		# must read, execute, and take screenshot
		if msg.type == TRAVERSAL_DATA:
			if msg.sender == "serv":
				resp_msg = Message("emu1",SCREENSHOT_READY,"Skype","test")
				self.send_message_to_node("serv",resp_msg.serializeMessage())
			else:
				# forward message to right emu
				msg.sender = "serv"
				self.send_message_to_node("emu1",msg.serializeMessage()) 


	def start(self):

		# Run the TCP server

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(),self.PORT))
		self.socket.listen(10)
		self.socket.setblocking(True)

		#listen for incoming connection from other docker nodes
		# TODO: figure out how to connect from outside docker network
		while True:
			print ("waiting")
			sys.stdout.flush()
			conn, addr = self.socket.accept()
			data = conn.recv(self.RECV_BUFFER)
			print ("data: " + data)
			self.parse_message(data)
			conn.close()

