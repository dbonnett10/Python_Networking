#************************************
# Dan Bonnett
# CMPSCI 381 Lab 3
#
# Honor Code: This work is my own unless otherwise cited.
#***********************************

# We need the time package to calculate round-trip times:
import time

from socket import *

host = 'localhost'
port = 12345
timeout = 1 # in seconds

# Create UDP client socket
# Note the use of SOCK_DGRAM for UDP datagram packet
clientsocket = socket(AF_INET, SOCK_DGRAM)

# Set socket timeout as 1 second
clientsocket.settimeout(1)

# Ping 10 times:
good = 0
avg = 0
for i in range(1,11):
    message = 'Ping '+ str(i)
    try:
        print "Sending: " + message
	# Save current time (this is the start time):
        start = time.time()
	# Send the UDP packet containing the ping message
        clientsocket.sendto(message,('localhost',12345))
	# Receive the server response
        message, address = clientsocket.recvfrom(1024)
        good += 1
	# Save current time (this is the end time)
        end = time.time()
	# Display the server response as an output
        print 'Server reply: Got it'
	# print round trip time (difference between end time and start time):
        elapsed = end - start
        print "Elapsed time = " + str(elapsed) + " seconds\n"
        avg = avg + elapsed
    except:
        # Server does not respond; assume packet is lost and print message:
        print 'Request Timed Out\n'
        continue

        i = i - 1

print str(good) + " Successful attempts"
print str(10-good) + " Unsuccessful attempts"
print "Average elapsed time: " + str(avg/good) + " seconds\n"

# Close the client socket
clientsocket.close()

