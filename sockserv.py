import socket               # Import socket module

import picamera
import time


camera = picamera.PiCamera()
camera.framerate = 20
print 'resolution is', camera.resolution
print "framerate is ", camera.framerate

print "setting up socket..."
socket = socket.socket()
# host = "192.168.2.1"
#host = "84.80.230.115"
host = ""
port = 82
socket.bind((host, port))
socket.listen(5)
print "socket ready %s : %s" % (host, port) 

while True:
    connection, addr = socket.accept()
    print 'Got connection from', addr
    # connection.send('Thank you for connecting')
    
    print "now starting camera recording"
    fileLikeObject = connection.makefile('rb')

    camera.brightness = 80
#    camera.start_recording(fileLikeObject, format='h264', intra_period = 1, inline_headers = False)
    camera.start_recording(fileLikeObject, format='h264', intra_period = 1, bitrate=2500000)
    # camera.wait_recording(300)
    #print "now stopping camera recording"
    # camera.stop_recording()

    # The constants SHUT_RD, SHUT_WR, SHUT_RDWR have the values 0, 1, 2,
    # respectively, and are defined in <sys/socket.h> since glibc-2.1.91.
    #print "now closing the connection"
    #connection.shutdown(2)
    #connection.close()            

socket.shutdown(2)
socket.close
