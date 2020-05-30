#!/bin/bash
# Start up script for RemoteMouse
trap 'kill %1' SIGINT
ADDRESSES=$(hostname -I)
ADDRESSES_ARRAY=($ADDRESSES)
HOST=${ADDRESSES_ARRAY[0]}
SERVER_PORT=8000
SOCKET_PORT=8888
python3 injectAddress.py $SOCKET_PORT $HOST
python3 socketServer.py $SOCKET_PORT $HOST & python3 rmServer.py rmApp:app $SERVER_PORT $HOST