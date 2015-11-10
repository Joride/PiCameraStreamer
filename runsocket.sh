#!/bin/bash

sudo python multistream.py &

# save the PID in a file
echo $! > multisocketID.sockID

echo "processID = $!"
