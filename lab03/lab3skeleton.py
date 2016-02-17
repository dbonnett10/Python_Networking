# YOUR NAME, HONOR CODE, LAB NUMBER

# We need the time package to calculate round-trip times:
import time

from socket import *

host = ...
port = ...
timeout = 1 # in seconds

# Create UDP client socket
# Note the use of SOCK_DGRAM for UDP datagram packet
clientsocket = socket(AF_INET, SOCK_DGRAM)

# Set socket timeout as 1 second
 ...

# Ping 10 times:
for i in range(1,11):
    message = ...
    try:
        print "Sending: " + message
	# Save current time (this is the start time):
          ...
	# Send the UDP packet containing the ping message
          ...
	# Receive the server response
          ...
	# Save current time (this is the end time)
         ...
	# Display the server response as an output
         ...
	# print round trip time (difference between end time and start time):
         ...
    except:
        # Server does not respond; assume packet is lost and print message:
           ...
        continue

# Close the client socket
clientsocket.close()

