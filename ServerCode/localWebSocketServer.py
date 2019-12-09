import asyncio
import websockets
import struct
import json


async def echo(websocket, path):
    print("START")
    async for message in websocket:
        print(message)
        await websocket.send(message)

start_server = websockets.serve(echo, "localhost", 9093)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
