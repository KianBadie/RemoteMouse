import asyncio
import websockets
import sys
import pyautogui

HOST = sys.argv[2]
PORT = int(sys.argv[1])

async def handler(websocket, path):
    while True:
        data = await websocket.recv()
        print(data)

start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()