import asyncio
import websockets
import sys
from pymouse import PyMouse
import json

HOST = sys.argv[2]
PORT = int(sys.argv[1])

async def handler(websocket, path):
    mouse = PyMouse()
    prev_coords = mouse.position()
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        headers = data['Headers']
        data = data['Data']
        if headers['Type'] == 'tap':
            current_x, current_y = mouse.position()
            mouse.click(current_x, current_y)
        elif headers['Type'] == 'move':
            current_x, current_y = mouse.position()
            mouse.move(current_x + data['changeX'], current_y + data['changeY'])

start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
print('Socket server listening on %s:%s' % (HOST, PORT))
asyncio.get_event_loop().run_forever()