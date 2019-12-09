import asyncio
import websockets
import struct
import json
import base64
import  socket
from PIL import Image




value = 5.1
ba = bytearray(struct.pack("f", value))


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('192.168.1.8', 980))

async def echo(websocket, path):
    print("START")
    async for message in websocket:
        print(message)
        await websocket.send(message)
        # sock.send(message.encode())

start_server = websockets.serve(echo, "", 9092)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
