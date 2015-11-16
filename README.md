# PiCameraStreamer
A Python script that starts a socket into which the PICamera can stream data.

This script is meant to run on a Raspberry Pi with a PiCamera installed. It will also need the pyhon package 'picamera'.

To start the picamera socket server:
  sudo ./runsocket.sh

All is good if you see something similar to:

  processID = 2374
  pi@raspberrypi: ~/
  camera rotation: 270
  camera on
  cameraresolution: (720, 480)
  framerate: 30
  brightness: 50
  socket set up
  
To stop the server:
sudo ./stopsocket.sh

To test this out, you can build the iOS-app found at https://github.com/Joride/sPiView.git and change the IP-number in there to match you raspberry's.

Joride, November 16, 2015.
