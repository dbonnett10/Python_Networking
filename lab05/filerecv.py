# VERY primitive file transfer. There is no protocol--when the
# server receives a connection request it immediately begins saving
# the data into a file. When data stop arriving or the connection
# times out, the file is closed and listening resumes.
# As a precaution, this can handle at most three file transfers before
# quitting. As a further precaution, no more than 10K bytes are allowed
# in any file.

import socket

# Create a server socket that listens for files:
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('',12345))
sock.listen(1)

# Wait at most 30 seconds between files; give up if no more requests.
# (This is just to show how different sockets can have different timeouts.)
sock.settimeout(30)

try: # We handle a server socket timeout at the "except:" line

  # Files are numbered consecutively as file0, file1, file2
  for filenum in range(3): # a real server might use "while True:"

    # Wait no more than 30 seconds for a new file to arrive
    connection,addr = sock.accept()
    print "connected to" + str(addr)

    # Wait no more than 1 second between blocks of data:
    connection.settimeout(1)

    # Create a new file:
    f = open('file'+str(filenum),'wb')

    try: # We handle a connection timeout at the "except:" line

      for kbytes in range(10): # For unbounded file size, use "while True:"
        block = connection.recv(1024)
        print "received block of size " + str(len(block))

        if len(block) == 0: # this happens when client closes socket
          break
        f.write(block)

      # No more data--close file and close connection
      f.close()
      connection.close()

    except socket.timeout: # connection is still open but no data arriving
        print "connection timed out"
        f.close()
        connection.close()

  # Server processed three files; quit.
  sock.close()

except socket.timeout: # server waited 30 seconds
  print "listener timed out"
  sock.close()
