import socket
import numpy as np
import cv2

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
print('Server started')
print(sock)
while True:
    client, addr = sock.accept()
    print('connected:', addr)
    while True:
        data = client.recv(1024).decode()
        if not data:
           break
        print(data)
        client.send("chto nibud".encode())

    client.close()
