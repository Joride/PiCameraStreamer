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
                writableObject.close()
    def flush(self):
        if self.items != None:            
            for writableObject in self.items:
                writableObject.flush()
    
    def __str__(self):
        return "MutliWrite instance with items: %s" % (self.items,)

def startRecordingIntoStream(fileLikeObject):
    if not fileLikeObject in multiWrite.items:
        multiWrite.items.append(fileLikeObject)

    if not camera.recording:
        print "camera starting now"
        camera.start_recording(multiWrite, format='h264', intra_period = 1, bitrate=0, quality=10)
        # camera.start_recording(multiWrite, format='h264', intra_period = 1, bitrate=2500000)
    else:
        print "camera already recording"

def stopRecordingIntoStream(fileLikeObject):
    if fileLikeObject in multiWrite.items:
        print "removing ", fileLikeObject
        multiWrite.items.remove(fileLikeObject)
    else:
        print "not removing ", fileLikeObject

    if len(multiWrite.items) == 0:
        print "no more listeners, stopping camera recording"
        camera.stop_recording()
    else:
        print "camera continues to record, number of items in multiWrite is ",  len(multiWrite.items)


def handleMessage(message, fileLikeObject):
    for byte in message:
        print "byte: ", ord(byte)

    print "-- end of message --"
    if ord(message[1]) == 0b00000001:
        startRecordingIntoStream(fileLikeObject)

    if ord(message[1]) == 0b00000000:
        stopRecordingIntoStream(fileLikeObject)

def listenForBytes(connection, multiWrite):
    fileLikeObject = connection.makefile('rb')
    
    while True:
        data = connection.recv(1024)
        
        if not data:
            print """%s has no more data, now considering it \
disconnected and closing the connection""" % (connection,)
            stopRecordingIntoStream(fileLikeObject)
            # maybe the connection did not actually disconnect
            # so we make sure it really is disconnected and in
            # this way the client knows we shut it down.
            try:
                connection.shutdown(2)  
                connection.close
            except Exception as instance:
                print type(instance)     # the exception instance
                print instance.args      # arguments stored in .args
                print instance           # __str__ allows args to be printed directly
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
                    currentMessage = None

                else:
                    currentMessage += byte



multiWrite = MultiWrite("/dev/null")

try:
    camera = picamera.PiCamera()
    camera.led = False
    print "camera on"
    print "cameraresolution: ", camera.resolution
    print "framerate: ", camera.framerate
except Exception as instance:
    print "Unable to enable the camera: %s" % (instance,)
    exit("1")

# setup a socket to listen on port 80
try:
    socket = socket.socket()
    host = ""
    port = 82
    socket.bind((host, port))
    socket.listen(5)
    print "socket set up"
except Exception as instance:
    print "Unable to setup up a listening scoket: %s" % (instance,)
    exit("1")

while True:
    try:
        connection, addr = socket.accept()
        worker1 = Thread(target=listenForBytes, args=(connection,multiWrite))
        worker1.setDaemon(True)
        worker1.start()

        print 'Got connection from %s %s' % (connection, addr)              

    except ValueError:
        print "ERROR IN MAIN WHILE LOOP: ", ValueError
        socket.shutdown(2)  
        socket.close
        break



        


        


        


