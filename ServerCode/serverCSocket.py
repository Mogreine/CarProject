import socket
import numpy as np
import cv2
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

sock = socket.socket()
sock.bind(('', 9091))
sock.listen(1)
print('Server started')
print(sock)
while True:
    client, addr = sock.accept()
    print('connected:', addr)
    while True:
        data = client.recv(2048).decode()


        if not data:
           break
        print(data)
        client.send("hello".encode())
    client.close()
    print("CLOSE")


