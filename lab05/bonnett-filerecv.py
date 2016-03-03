# ************************************
# Dan Bonnett
# CMPSCI 381 Lab 5
# Honor Code: This work is my own unless otherwise cited
# ************************************

import socket

MAXFILES = 3 # receive at most this many files
MAXBLOCKS = 1000 # files can't exceed 1000 * 1024 bytes
SERVERTIMEOUT = 30 # after 30 seconds with no requests, shut down server
length = 0  # initializing length to zero

# Create a server socket that listens for files:
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('',12345))
sock.listen(1)
sock.settimeout(SERVERTIMEOUT)

try: # We handle a server socket timeout at the "except:" line

  for filenum in range(MAXFILES):

    connection,addr = sock.accept()
    print "DEBUG: connected to" + str(addr)
    connection.settimeout(1)

    # Receive the "PUT" message, extract filename and filesize
    put_message = connection.recv(1024)  # receive the PUT message
    txt = put_message.split()  # split the PUT message
    filename = txt[1]  # save the filename
    filesize = int(txt[2])  # save the file size
    print "DEBUG: received request " + str(put_message)  # print Debugging message

    #send the OK message
    connection.send('OK')

    # Create a new file:
    f = open('_'+filename,'wb')
    print "DEBUG: Saving "+filename+" in _"+filename

    try:

      # Loop to receive data and send back cumulative bytes received:
      while True:
            block = connection.recv(1024) #receive the block
            length += len(block)  #increment length by the size of each block received
            connection.send(str(length) + ' Bytes')  #send the current number of bytes received
            f.write(block)

            # if the number of bytes is greater than the filesize
            # then we break
            if length >= filesize:
                break

            # print the total number of bytes received
      print "DEBUG: Successfully received " + str(length) + " bytes"


      # No more data--close file, send final OK message, and close connection
      f.close()
      connection.send("OK Received " + str(length) + " bytes")
      connection.close()

    except socket.timeout: # This shouldn't happen!
        print "DEBUG: connection timed out (this shouldn't happen!)"
        f.close()
        connection.close()

  sock.close() # Close after MAXFILES files have been received

except socket.timeout:
  print "DEBUG: listener timed out"
  sock.close()
