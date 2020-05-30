#!/bin/bash
# Start up script for RemoteMouse
ADDRESSES=$(hostname -I)
ADDRESSES_ARRAY=($ADDRESSES)
HOST=${ADDRESSES_ARRAY[0]}
SERVER_PORT=8000
SOCKET_PORT=8888
python3 rmServer.py rmApp:app $SERVER_PORT $HOST