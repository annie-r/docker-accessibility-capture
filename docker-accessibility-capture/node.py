import socket
import sys
from message import *

class Node:
	def __init__(self, port):
		self.RECV_BUFFER = 4096
		self.PORT = 8875
		print ("created")


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
		while True:
			print ("waiting")
			sys.stdout.flush()
			conn, addr = self.socket.accept()
			data = conn.recv(self.RECV_BUFFER)
			print ("data: " + data)
			self.parse_message(data)
			'''
			self.send_message_to_node("cont1",msg.type)
			sys.stdout.flush()
			if (socket.gethostname() == "serv"):
				self.send_message_to_node("cont1","from serv")
				'''
			conn.close()

	def listen(self):
		None

if __name__ == '__main__':
	node = Node(8888)
	node.run()