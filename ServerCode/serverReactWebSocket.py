import asyncio
import websockets
import struct
import json
import base64
import  socket
from PIL import Image

old_r = 0
old_a = 0


value = 5.1
ba = bytearray(struct.pack("f", value))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.9', 9081))
print("SOCKET CONNECT")

# while True:
#     q = input()
#     lst = q.split()
#     r = float(lst[0])
#     a = float(lst[1])
#     r_encode = bytearray(struct.pack("f", r))
#     a_encode = bytearray(struct.pack("f", a))
#     sock.send(r_encode)
#     sock.send(a_encode)
#     print("send out")


async def echo(websocket, path):
    print("START CONVERSATION")
    async for message in websocket:
        print(message)
        lst = message.split()
        if lst[0] == "NaN":
            lst[0] = old_r
        if lst[1] == "NaN":
            lst[1] = old_a
            print("NET NANA")
        r = float(lst[0])
        a = float(lst[1])
        old_r = r
        old_a = a
        r_encode = bytearray(struct.pack("f", r))

        a_encode = bytearray(struct.pack("f", a))
        await websocket.send(message)
        sock.send(r_encode)
        sock.send(a_encode)



start_server = websockets.serve(echo, "", 9092)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
