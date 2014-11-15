#!/bin/bash

# get the sockID
sockID=$(cat multisocketID.sockID)

# kill the process
kill $sockID

rm ./multisocketID.sockID