#*********************************
# Dan Bonnett
# CMPSCI 381 Lab 11
# Python Cache
# Honor Code: This work is my own unless otherwise cited.
#*********************************

import socket

# Create a "listening socket" that waits for requests:
listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind(('', 12345)) # runs on localhost
listenSocket.listen(1)
SERVERTIMEOUT = 60
listenSocket.settimeout(SERVERTIMEOUT)

while True:

  # New client (from Firefox or a terminal "telnet" command):
  tcpSocket,addr = listenSocket.accept()
  print "Server connected to " + str(addr)

  # Client sends "GET http://hostname/filename HTTP/1.1" :
  getRequest = tcpSocket.recv(1024)
  print "Server received " + str(getRequest)

  # Extract website hostname and the name of the file (lab 9):
  temp1 = getRequest.partition('http://')
  tempHost = temp1[2]
  temp2 = tempHost.split()
  temp3 = temp2[0].partition('/')
  realHost = temp3[0]
  reqFile = temp3[1] + temp3[2]

  cachedStr = temp2[0].replace("/", "-slash-")

  print "Requested host: " + str(realHost)
  print "Requested file: " + str(reqFile)


  # Open a new socket to port 80 of the specied hostname:
  webSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  webSocket.connect((realHost, 80))


  try:
      cachefile = open(cachedStr, 'rb')
      cached = True
  except:
      cachefile = open(cachedStr, 'wb')
      cached = False
  if cached:
      print "Sending cache file " + str(cachedStr) + " to " + str(addr)

      while True:
          block = cachefile.read(1024)
          if not block:
              break

          tcpSocket.send(block)

  else:
      webSocket.send('GET '+reqFile+' HTTP/1.0\n\n')
      cfile = webSocket.makefile('rb' ,0)
      webSocket.send(str(cfile))
      print "creating cache file " + str(cachedStr)
      print "requesting file " + str(reqFile) + " from " + str(realHost)
      print "sending " + str(reqFile) + " to " + str(addr)

      while True:
          block = cfile.read(1024)
          if not block:
              break
          tcpSocket.send(block)



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
