import picamera

class MutliWrite:
    
    def write(param1, param2):
        print "%s" % (param1,)
    
    def __str__(self):
        return "MutliWrite instance"
        

multiWrite = MutliWrite()
camera = picamera.PiCamera()
camera.start_recording(multiWrite, format='h264', intra_period = 1, bitrate=2500000)
camera.wait_recording(5)
camera.stop_recording()