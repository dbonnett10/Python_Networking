from socket import *
import time

# Identify the web server:
serverName = 'localhost'
serverPort = 12345

print "First test: not enough fields in first line:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html\nHost: localhost\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "############################"

print "Second test: GET misspelled:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('Get /page1.html HTTP/1.1\nHost: localhost\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "############################"

print "Third test: Missing Host: header:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html HTTP/1.1\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "############################"

print "Fourth test: Misspelled Host: header:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html HTTP/1.1\nHOST: localhost\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "############################"

print "Fifth test: wrong number of fields in Host: header:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html HTTP/1.1\nHost:localhost\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "############################"

print "Sixth test: wrong number of fields in Host: header:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html HTTP/1.1\nHost: localhost garbage\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "############################"

#Test that I added
print "Seventh test: incorrect Host name:"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html HTTP/1.1\nHost: garbage\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()

print "#############################"

print "eighth test: successful request"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clientSocket.send('GET /page1.html HTTP/1.1\nHost: localhost\n\n')

time.sleep(2) # We need some delay here!

result = clientSocket.recv(2048)
print result
clientSocket.close()
