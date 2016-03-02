# *************************************
# Dan Bonnett
# CMPSCI 381 Lab 5
# Honor Code: This work is my own unless otherwise cited
# *************************************

import socket
import os.path

# Ask user for file name:
filename = raw_input("File to transfer: ")

try:
    # Open the file, get its size
        f = open(filename, 'rb')
        filesize = os.path.getsize(filename)

    # Create socket and connect to the socket created by filerecv.py:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('', 12345))


    # Send the PUT message
        s.send("PUT " + filename + " " + str(filesize))

    # Receive and print the "OK" message:
        ok_message = s.recv(1024)
        print ok_message

    # Loop: send the file in blocks of size 1024; after each send,
    # receive a reply from the server and print it.
        while True:
            block = f.read(1024)

            if not block:
                print "DEBUG: reached end of file"
                break

            # send the block
            s.send(block)

            # receive and print the byte message (e.g. 1024 bytes)
            byte_message = s.recv(1024)
            print byte_message

    # Receive and print final "OK Received...." message, close
    # file, close socket
        print "DEBUG: closing file " + filename
        final_message = s.recv(1024)  # receive the final message
        print final_message
        f.close()  # close the file
        s.close()  # close the socket

except socket.error:
    print "socket error -- can't find server"

except IOError:
    print "no such file"
