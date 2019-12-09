import socket
import struct
import numpy as np
import cv2
import asyncio
import websockets
from PIL import Image

value = 5.1
ba = bytearray(struct.pack("f", value))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.8', 980))
while True:
    size = sock.recv(4)
    sizeInt = int.from_bytes(size,byteorder='big', signed=False)

    data = sock.recv(sizeInt)


    nparr = np.fromstring(data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR in OpenCV 3.1
    if img_np is None:
        continue
    print(sizeInt)
    cv2.imshow('image',img_np)
    cv2.waitKey(50)

sock.close()







