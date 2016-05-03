#*********************************
# Dan Bonnett
# CMPSCI 381 Lab 12
# Python Proxy Server with a forbidden file policy.
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

# boolean used for determining a forbidden file
badRequest = False


while True:

  # New client (from Firefox or a terminal "telnet" command):
  tcpSocket,addr = listenSocket.accept()
  print "Server connected to " + str(addr)


  # Client sends "GET http://hostname/filename HTTP/1.1" :
  getRequest = tcpSocket.recv(1024)
  print "Server received " + str(getRequest)


  #**********************************************************
  # Extract website hostname and the name of the file (lab 9):
  #**********************************************************
  temp1 = getRequest.partition('http://')
  tempHost = temp1[2]
  temp2 = tempHost.split()
  tempReq = temp2[0]  # used for bad file detection, holds realHost + reqFile
  temp3 = temp2[0].partition('/')
  realHost = temp3[0]  # this variable holds the actual host name
  reqFile = temp3[1] + temp3[2]  # this variable hold the requested file

  cachedStr = temp2[0].replace("/", "-slash-")

  print "Requested host: " + str(realHost)
  print "Requested file: " + str(reqFile)


  # Open a new socket to port 80 of the specified hostname:
  webSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  webSocket.connect((realHost, 80))


  #****************************************************************
  # determine whether or not the client requested a forbidden file
  # and returns an appropriate response if the file is forbidden
  #****************************************************************
  forbidden = ['reddit', 'jwenskovitch', 'youtube', 'apple']
  for s in forbidden:
      if s in tempReq:
          badRequest = True
          if badRequest:
              badfile = open("Bad.html", 'rb')
              print "Received request for forbidden file"
              print "Sending cached file " + str(badfile.name) + " to " + str(addr)

          while True:
              blocks = badfile.read(1024)
              if not blocks:
                  break
              tcpSocket.send(blocks)

          badfile.close()


 #**************************************************************
 # Handles the cache operations from lab 11
 # However, this time it must account for a forbidden file
 #**************************************************************
  try:
         cachefile = open(cachedStr, 'rb')
         cached = True
  except:
         cachefile = open(cachedStr, 'wb')
         cached = False
  if cached and badRequest is False:
         print "Sending cache file " + str(cachedStr) + " to " + str(addr)

         while True:
             block = cachefile.read(1024)
             if not block:
                 break

             if badRequest is False:
                 tcpSocket.send(block)
             else:
                 break

  else:
     webSocket.send('GET '+reqFile+' HTTP/1.0\n\n')
     cfile = webSocket.makefile('rb' ,0)
     if badRequest is False:
       print "creating cache file " + str(cachedStr)
       print "requesting file " + str(reqFile) + " from " + str(realHost)
       print "sending " + str(reqFile) + " to " + str(addr)

     while True:
          block = cfile.read(1024)
          if not block:
              break
          if badRequest is False:
              tcpSocket.send(block)
              cachefile.write(block)
          else:
              break
     cachefile.close()


  # close your webSocket and tcpSocket; leave open the listenSocket
  webSocket.close()
  tcpSocket.close()
