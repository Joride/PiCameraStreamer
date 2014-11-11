import socket               # Import socket module

import picamera
import time

camera = picamera.PiCamera()

print "setting up socket..."
socket = socket.socket()
# host = "192.168.2.1"
#host = "84.80.230.115"
host = ""
port = 82
socket.bind((host, port))
socket.listen(5)
print "socket ready %s : %s" % (host, port) 

kBeginOfMessage  = 0b10000000
kEndOfMessage    = 0b11000000

def startRecordingIntoStream(stream):
    print "now starting camera recording"
    camera.framerate = 20
    print 'resolution is', camera.resolution
    print "framerate is ", camera.framerate
    camera.brightness = 80

    fileLikeObject = connection.makefile('rb')
    camera.start_recording(fileLikeObject, format='h264', intra_period = 1, bitrate=2500000)
    print "camera is now recording"

def stopRecordingIntoStream(stream, camera):
    print "now stopping camera recording"
    camera.stop_recording()

def handleMessage(message):
    for byte in message:
        print "byte: ", ord(byte)

    print "-- end of message --"
    if ord(message[1]) == 0b00000001:
        startRecordingIntoStream(connection)

    if ord(message[1]) == 0b00000000:
        stopRecordingIntoStream(connection, camera)


while True:
    try:
        connection, addr = socket.accept()
        print 'Got connection from %s %s' % (connection, addr)

        currentMessage = None
        while True:
            data = connection.recv(1024)
            
            for byte in data:
                binaryByte  = ord(byte)
                if binaryByte == kBeginOfMessage:
                    currentMessage = byte

                elif binaryByte == kEndOfMessage:
                    currentMessage += byte
                    handleMessage(currentMessage)
                    currentMessage = None

                else:
                    currentMessage += byte
                     

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

