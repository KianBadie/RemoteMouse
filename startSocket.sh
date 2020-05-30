#!/bin/bash
# Start up script for RemoteMouse
ADDRESSES=$(hostname -I)
ADDRESSES_ARRAY=($ADDRESSES)
HOST=${ADDRESSES_ARRAY[0]}
SOCKET_PORT=8888
python3 socketServer.py $SOCKET_PORT $HOST
