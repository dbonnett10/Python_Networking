#*********************************
# Dan Bonnett
# CMPSCI 381 Lab 10
# Python Server
# Honor Code: This work is my own unless otherwise cited.
#*********************************

import socket

# Create a "listening socket" that waits for requests:
listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listenSocket.bind(('', 12345)) # runs on localhost
listenSocket.listen(1)
SERVERTIMEOUT = 50
listenSocket.settimeout(SERVERTIMEOUT)

while True:

  # New client (from Firefox or a terminal "telnet" command):
  tcpSocket,addr = listenSocket.accept()

  # Client sends "GET http://hostname/filename HTTP/1.1" :
  getRequest = tcpSocket.recv(1024)

  # Extract website hostname and the name of the file (lab 9):
  temp1 = getRequest.partition('http://')
  tempHost = temp1[2]
  temp2 = tempHost.split()
  temp3 = temp2[0].partition('/')
  realHost = temp3[0]
  reqFile = temp3[1] + temp3[2]


  # Open a new socket to port 80 of the specied hostname:
  webSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  webSocket.connect((realHost, 80))


  # Send a "GET" request for the file name (use HTTP/1.0 for this);
  # don't forget the two '\n\n' at the end of the request!
  # (The file "test.py" from lab 2 shows examples of these; however,
  # you can dispense with the "Localhost: header" when using HTTP/1.0.)

  webSocket.send('GET '+reqFile+' HTTP/1.0\n\n')


  # Receive the reply from the web server--it will be a (possibly
  # lengthy) file, so receive it as a file rather than multiple blocks

  remoteFile = webSocket.makefile('rb', 0)
  while True:
      block = remoteFile.read(1024)
      if not block:
          break
      tcpSocket.send(block)

      byte_msg = webSocket.recv(1024)
      tcpSocket.send(byte_msg)

  # close your webSocket and tcpSocket; leave open the listenSocket
  webSocket.close()
  tcpSocket.close()
