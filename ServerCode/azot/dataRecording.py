import cv2
import numpy as np
import base64
import websockets
import asyncio
import requests
import detector
import time

import xlwt
from scipy import ndimage

url = "http://192.168.1.3/capture"


async def echo(websocket, path):
    print("START CONVERSATION")
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Test', cell_overwrite_ok=True)
    i = 0
    try:
        async for message in websocket:
            print(message)
            params = message.split(' ')
            start_time = time.time()
            imgResp = requests.get(url, data={"x": '{:.6}'.format(params[0]), "y": '{:.6}'.format(params[1]),
                                              "pid": params[2]})
            elapsed_time = time.time() - start_time
            requests_time1 = int(elapsed_time * 1000)
            print(f'Request time: {requests_time1} ms')
            ws.write(i, 0, i)
            ws.write(i, 1, requests_time1)
            i = i + 1
            imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            img = ndimage.rotate(img, -90)

            if params[3] == "1":
                start_time = time.time()
                img = detector.find_persons(img)
                elapsed_time = time.time() - start_time
                print(f'ML time: {elapsed_time}')

            # processed_string = base64.b64encode(img)
            retval, buffer = cv2.imencode('.jpg', img)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            # print(jpg_as_text.decode('utf-8'))
            # print(jpg_as_text)
            # cv2.imshow('test', img)
            # cv2.waitKey(1)
            await websocket.send(jpg_as_text)

    except Exception:
        print("STOP CONVERSATION WITH ERROR")
        wb.save('my_file.xls')
        asyncio.get_event_loop().close()
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


print('Started')

start_server = websockets.serve(echo, "", 9092)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()