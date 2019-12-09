import asyncio
import websockets
import struct

value = 5.1
ba = bytearray(struct.pack("f", value))
value1 = 1.3
print(ba," ",len(ba))
ba1 = bytearray(struct.pack("f", value1))
value2 = 23.1
print(ba1," ",len(ba1))
ba2 = bytearray(struct.pack("f", value2))
print(ba2," ",len(ba2))


async def echo(websocket, path):
    print("START")
    async for message in websocket:
        print(message)
        await websocket.send(ba)

start_server = websockets.serve(echo, "", 9091)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()