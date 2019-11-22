import asyncio
import websockets
import struct
import json




value = 5.1
ba = bytearray(struct.pack("f", value))

data = {
        "name": "Chislo",
        "value": ba
}

async def echo(websocket, path):
    print("START")
    async for message in websocket:
        print(message)
        await websocket.send(data)

start_server = websockets.serve(echo, "", 9092)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
