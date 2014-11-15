#!/bin/bash

sudo python multisocket.py &

# save the PID in a file
echo $! > multisocketID.sockID