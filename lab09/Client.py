#*****************************
# Dan Bonnett
# CMPSCI 381 Lab 9
# Simple TCP client:
# Honor Code: This work is my own unless otherwise cited.
#*****************************

import socket
msg = raw_input('what message do you want to send? ')
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(('',12345))
socket.send(msg)
reply = socket.recv(1024)
print "server replied: " + reply
socket.close()
