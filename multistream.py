import socket
import picamera
from Queue import Queue
from threading import Thread

kBeginOfMessage  = 0b10000000
kEndOfMessage    = 0b11000000

# This class exists so that the camera can use it as the file
# fileLikeObject it needs to write to. This object will then
# write the data into multiple clients.
class MultiWrite(file):
    items = []
    
    def write(self, data):
        if self.items != None:            
            for writableObject in self.items:
                writableObject.write(data)

    def close(self):
        if self.items != None:            
            for writableObject in self.items:
                writableObject,close()
    
    def flush(self):
        if self.items != None:          
            for writableObject in self.items:
               writableObject.flush()
    
    def __str__(self):
        return "MutliWrite instance with items: %s" % (self.items,)

def startRecordingIntoStream(fileLikeObject):
    if not fileLikeObject in multiWrite.items:
        print "appending %s to %s items" % (fileLikeObject, multiWrite)
        multiWrite.items.append(fileLikeObject)
    else:
        print "%s already in multiWrite.items: %s" % (fileLikeObject, multiWrite.items)

    if not camera.recording:
        print "camera starting now"
        #camera.start_recording(multiWrite, format='h264', intra_period = 1, bitrate=0, quality=10)
        camera.start_recording(multiWrite, format='h264', intra_period = 1, bitrate=1200000)
    else:
        print "camera already recording"

def stopRecordingIntoStream(fileLikeObject):
    if fileLikeObject in multiWrite.items:
        print "removing ", fileLikeObject
        multiWrite.items.remove(fileLikeObject)
    else:
        print "now removing ", fileLikeObject

    if len(multiWrite.items) == 0:
        print "no more listeners, stopping camera recording"
        camera.stop_recording()
    else:
        print "camera continues to record, number of items in multiWrite is %s" % (len(multiWrite.items),)

def handleMessage(message, fileLikeObject):
    for byte in message:
        print "byte: ", ord(byte)

    print "-- end of message --"

    if ord(message[1]) == 0b00000001:
        startRecordingIntoStream(fileLikeObject)

    if ord(message[1]) == 0b00000000:
        stopRecordingIntoStream(fileLikeObject)

def listenForBytes(connection, multiWrite):
    fileLikeObject = connection.makefile('sb')

    while True:
        data = connection.recv(1026)
        currentMessage = None

        if not data:
            print "%s has no more data, now considering it disconnected and closing the connection""" % (connection,)
            stopRecordingIntoStream(fileLikeObject)

            # maybe the connection did not actually disconnect
            # so we make sure it really is disconnected and in
            # this way the client knows we shut down
            try:
                connection.shutdown(2)
                connection.close
            except Exception as instance:
                # print type(instance)    # the exception instance
                # print instance.args     # arguments stored in .args
                # print instance          # __str__ logs args to be printed directly
                print "Unable to close a connection that returns not more data: %s" % (instance,)

            break

        else:
            for byte in data:
                binaryByte  = ord(byte)
                if binaryByte == kBeginOfMessage:
                    currentMessage = byte
            
                elif binaryByte == kEndOfMessage:
                    currentMessage += byte
                    handleMessage(currentMessage, fileLikeObject)
                    currentMessage = []
            
                else:
                    if currentMessage !=  None:
                        currentMessage += byte
                    else:
                        print "Programming error: trying to appent a byte to the currentMessage, but there is no currentmessage yet."


# create a file-object that writes into the void (well it actually,
# writes into the sub-items, so this string is not really relevant).
multiWrite = MultiWrite("/dev/null")

try:
    camera = picamera.PiCamera()
    camera.led = False
    camera.framerate = 12
    #camera.brightness = 80
    print "camera on"
    print "cameraresolution: %s" % (camera.resolution,)
    print "framerate: %s" % (camera.framerate,)
    print "brightness: %s" % (camera.brightness,)
except Exception as instance:
    print "Unable to enable the camera: %s" % (instance,)
    exit("1")

# setup a socket to listen on port 80
try:
    socket = socket.socket()
    host = ""
    port = 82
    socket.bind((host, port))
    socket.listen(82)
    print "socket set up"
except Exception as instance:
    print "Unable to setup a listening socket: %s" % (instance,)
    exit("1")


# this will run forever until the the socket closes / client disconnects / error in socket occurs
while True:
    try:
        connection, addr = socket.accept()
        worker = Thread(target=listenForBytes, args=(connection,multiWrite))
        worker.setDaemon(True)
        worker.start()

        print "Got connection from %s %s" % (connection, addr)              

    except ValueError:
        print "ERROR IN MAIN WHILE LOOP: ", ValueError
        print "Now shutting down socket and closing it."

        # The constants SHUT_RD, SHUT_WR, SHUT_RDWR have the values 0, 1, 2,
        # respectively, and are defined in <sys/socket.h> since glibc-2.1.91.
        socket.shutdown(2)  
        socket.close
        break









