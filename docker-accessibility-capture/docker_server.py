# Socket server in python using select function
#
import socket, select
from message import *
from node import Node
from docker_network import NetworkNode 
import sys

if __name__ == '__main__':
    nn = Node(8888)
    sys.stdout.flush()
    nn.start()


    # node = Node(8888)
    # node.setup_incoming()
    # while True:
    #     print "listening"
    #     res = node.listen()
    #     node.send_message_to_node("cont1",res)
    #     '''

    # CONNECTION_LIST = []    # list of socket clients
    # RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    # PORT = 8888
         
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # # this has no effect, why ?
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.bind(("0.0.0.0", PORT))
    # server_socket.listen(10)
    # # Add server socket to the list of readable connections
    # CONNECTION_LIST.append(server_socket)

    # print "Chat server started on port " + str(PORT)


    # while 1:
    #     try:
    #         # Get the list sockets which are ready to be read through select
    #         read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

    #         for sock in read_sockets:
                 
    #             #New connection
    #             if sock == server_socket:
    #                 # Handle the case in which there is a new connection recieved through server_socket
    #                 sockfd, addr = server_socket.accept()
    #                 CONNECTION_LIST.append(sockfd)
    #                 print "Client (%s, %s) connected" % addr
                     
    #             #Some incoming message from a client
    #             else:
    #                 # Data recieved from client, process it
    #                 try:

    #                     #In Windows, sometimes when a TCP program closes abruptly,09
    #                     # a "Connection reset by peer" exception will be thrown
    #                     data = sock.recv(RECV_BUFFER)
    #                     sock.send(data)
    #                     # echo back the client message
    #                     if data == "test":
    #                         sock.send('Good ... ' + data)
    #                     else:
    #                         msg = Message()
    #                         msg.deserialize(data)
    #                         #sock.send(msg.type)
    #                         if msg.type == SCREENSHOT:
    #                             sock.send("SCREENSHOT RECV!" + data)
    #                         sock.send(data)
    #                         # parse message
    #                         # message has: who it's from, type,  
    #                         #from

    #                     else:
    #                         fname = "data/screen.png"
    #                         fp = open (fname,'w')
    #                         while True:
    #                             strng = client_socket.recv(512)
    #                             if not strng:
    #                                 break
    #                             fp.write(strng)
    #                         fp.close()
    #                         sock.send('Done ')
    #                     '''
    #                     print "done"
                     
    #                 # client disconnected, so remove from socket list
    #                 except:
    #                     #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
    #                     print "Client (%s, %s) is offline" % addr
    #                     sock.close()
    #                     CONNECTION_LIST.remove(sock)
    #                     continue
    #     except KeyboardInterrupt:
    #         for sock in CONNECTION_LIST:
    #             sock.close()     
    # server_socket.close()