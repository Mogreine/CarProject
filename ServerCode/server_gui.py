import cv2
import numpy as np
import base64
import websockets
import asyncio
import requests
#import detector
import time

import xlwt
from scipy import ndimage

from tkinter import *

window = Tk()
window.title('Пишем историю для сервера')
window.geometry('720x960+300+100')
window.configure(bg='gray10')

url = StringVar()
url.set("http://192.168.1.2/capture")
port = StringVar()
port.set(9092)

async def echo(websocket, path):
    output_text.insert(END, "START CONVERSATION\n")
    output_text.see(END)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Test', cell_overwrite_ok=True)
    i = 0
    try:
        async for message in websocket:
            output_text.insert(END, message)
            output_text.see(END)
            params = message.split(' ')
            start_time = time.time()
            imgResp = requests.get(url.get(), data={"x": '{:.6}'.format(params[0]), "y": '{:.6}'.format(params[1]), "pid": params[2]})
            elapsed_time = time.time() - start_time
            requests_time1 = int(elapsed_time * 1000)
            output_text.insert(END, f'Request time: {requests_time1} ms\n')
            output_text.see(END)
            ws.write(i, 0, i)
            ws.write(i, 1, requests_time1)
            i = i + 1
            imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            img = ndimage.rotate(img, -90)

            if params[3] == "1":
                start_time = time.time()
                #img = detector.find_persons(img)
                elapsed_time = time.time() - start_time
                output_text.insert(END, f'ML time: {elapsed_time}\n')
                output_text.see(END)

            # processed_string = base64.b64encode(img)
            retval, buffer = cv2.imencode('.jpg', img)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            # print(jpg_as_text.decode('utf-8'))
            # print(jpg_as_text)
            # cv2.imshow('test', img)
            # cv2.waitKey(1)
            await websocket.send(jpg_as_text)

    except TimeoutError:
        output_text.insert(END, "STOP CONVERSATION WITH ERROR\n")
        output_text.see(END)
        wb.save('my_file.xls')
        asyncio.get_event_loop().close()
        run()


def run():
    # outptut_text.set('Started\n')
    state['bg'] = 'brown1'
    start_server = websockets.serve(echo, "", port.get())
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def stop():
    state['bg'] = 'gray20'
    asyncio.get_event_loop().close()
    output_text.delete(1.0, END)

def focus_btn(event):
    event.widget['bg'] = 'gray50'

def defocus_btn(event):
    event.widget['bg'] = 'gray30'

url_label = Label(text='url:',
                  font='Arial 14',
                  width=6,
                  bg='gray80')
url_label.place(relx=.11, rely=.06)

url_entry = Entry(font='Arial 14',
                   width='27',
                   bg='gray80',
                   fg='gray20',
                   textvariable=url)
url_entry.place(relx=.22, rely=.06)

port_label = Label(text='port:',
                  font='Arial 14',
                  width=6,
                  bg='gray80')
port_label.place(relx=.11, rely=.11)

port_entry = Entry(font='Arial 14',
                   width='27',
                   bg='gray80',
                   fg='gray20',
                   textvariable=port)
port_entry.place(relx=.22, rely=.11)

run_btn =  Button(text='Погнали, работяги',
                         font='Arial 14',
                         width='33',
                         relief='ridge',
                         bg='gray30',
                         fg='gray80',
                         activebackground ='gray50',
                         command=run)
run_btn.place(relx=.11, rely=.16)
run_btn.bind('<Enter>', focus_btn)
run_btn.bind('<Leave>', defocus_btn)

stop_btn =  Button(text='Стоять, работяги',
                         font='Arial 14',
                         width='33',
                         relief='ridge',
                         bg='gray30',
                         fg='gray80',
                         activebackground ='gray50',
                         command=stop)
stop_btn.place(relx=.11, rely=.22)
stop_btn.bind('<Enter>', focus_btn)
stop_btn.bind('<Leave>', defocus_btn)

scroll = Scrollbar()
scroll.pack(side=RIGHT, fill=Y)

state = Label(width='23',
              height='12',
              bg='gray20')
state.place(relx=.65, rely=.06)

output_text = Text(font='Arial 14',
                        width='50',
                        height='30',
                        bg='gray80',
                        fg='gray20',
                        wrap=WORD,
                        yscrollcommand=scroll.set)
output_text.place(relx=.11, rely=.27)
scroll.config(command=output_text.yview)

window.mainloop()