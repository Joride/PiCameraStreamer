import socket               # Import socket module

import picamera
import time

print "setting up socket..."
socket = socket.socket()
# host = "192.168.2.1"
#host = "84.80.230.115"
host = ""
port = 82
socket.bind((host, port))
socket.listen(5)
print "socket ready %s : %s" % (host, port) 

def startRecordingIntoStream(stream):
    print "now starting camera recording"
    camera = picamera.PiCamera()
    camera.framerate = 20
    print 'resolution is', camera.resolution
    print "framerate is ", camera.framerate
    camera.brightness = 80

    fileLikeObject = connection.makefile('rb')
    camera.start_recording(fileLikeObject, format='h264', intra_period = 1, bitrate=2500000)
    # camera.wait_recording(600)
    print "camera is now recording"

    return camera

def stopRecordingIntoStream(stream, camera):
    print "now stopping camera recording"
    camera.stop_recording()

while True:
    try:
        connection, addr = socket.accept()
        print 'Got connection from %s %s' % (connection, addr)

        length = None
        buffer = ""
        while True:
            data = connection.recv(1024)
            
            
            for byte in data:
                print "byte is: ", ord(byte)
                if ord(byte) == 1<<7:
                    print "recording data"
                    camera = startRecordingIntoStream(connection)
                elif ord(byte) == 1<<6:
                     print "stopping recording"
                     stopRecordingIntoStream(connection, camera)


    except ValueError:
        print "ERROR: ", ValueError
        socket.shutdown(2)
        socket.close
        break


# The constants SHUT_RD, SHUT_WR, SHUT_RDWR have the values 0, 1, 2,
# respectively, and are defined in <sys/socket.h> since glibc-2.1.91.
# print "now closing the connection"
# connection.shutdown(2)
# connection.close()            

