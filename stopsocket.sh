#!/bin/bash

# get the sockID
sockID=$(cat multisocketID.sockID)

# kill the process
kill $sockID

# delete the handle to the process we just killed
rm ./multisocketID.sockID