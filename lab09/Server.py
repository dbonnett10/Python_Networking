#**************************
# Dan Bonnett
# CMPSCI 381 Lab 9
# Simple TCP server:
# Honor Code: This work is my own unless otherwise cited.
#**************************

import socket
listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # creating a TCP socket
listenSocket.bind(('', 12345))  # binding the socket to port 12345
listenSocket.listen(1)  # telling the socket to be ready to receive

while True:
  tcpSocket,addr = listenSocket.accept()
  print "server connected to " + str(addr)
  receivedMsg = tcpSocket.recv(1024)
  temp1 = receivedMsg.partition('http://')
  tempHost = temp1[2]
  temp2 = tempHost.split()
  temp3 = temp2[0].partition('/')
  realHost = temp3[0]
  print "requested host: " + str(realHost)
  rfile = temp3[1] + temp3[2]
  print "requested file: " + str(rfile)
  #print "received: " + receivedMsg
  tcpSocket.send('You requested ' + rfile + ' from ' + realHost)
  tcpSocket.close()
