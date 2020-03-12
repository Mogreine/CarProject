from tkinter import *
import cv2
from PIL import Image, ImageTk
import json
import detector
import management
import time

window = Tk()
window.title('Пишем историю')
window.geometry('1080x720+300+100')
window.configure(bg='gray10')

name = StringVar()
state = StringVar()
state.set('Ответ убил')
frames = fps = t = 0
fps_str = StringVar()
fps_str.set(0.0)
video_capture = cv2.VideoCapture(0)

def show_frame():
    global frames, fps, t
    frames += 1
    if frames > 10:
        fps = frames / (time.time() - t)
        fps_str.set(f'{round(fps, 1)} fps')
    frame = video_capture.read()[1]
    frame = cv2.flip(frame, 1)
    cv2image = detector.find_persons(frame)
    cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, show_frame)

def fill_listbox():
    with open('persons.json') as persons:
        data = json.load(persons)
        for i in data['names']:
            known_persons_lbox.insert(END, i)

def add_person_click():
    if name.get() != '':
        frame = video_capture.read()[1]
        frame = cv2.flip(frame, 1)
        exist = management.add_person(name.get(), frame)
        if exist == 0:
            known_persons_lbox.insert(END, name.get())
            state.set(f'Персона {name.get()} добавлена')
        elif exist == 1:
            state.set(f'Персона {name.get()} обновлена')
        else:
            state.set('Лицо не обнаружено')
        name.set('')
    else:
        state.set('Введите имя персоны')

def add_person_file_click():
    from tkinter import filedialog
    file_name = filedialog.askopenfilename(filetypes=[('PNG images', '.png'), ('JPEG images', '.jpg')])
    if file_name != '':
        if name.get() != '':
            image = cv2.imread(file_name)
            exist = management.add_person(name.get(), image)
            if exist == 0:
                known_persons_lbox.insert(END, name.get())
                state.set(f'Персона {name.get()} добавлена')
            elif exist == 1:
                state.set(f'Персона {name.get()} обновлена')
            else:
                state.set('Лицо не обнаружено')
            name.set('')
        else:
            state.set('Введите имя персоны')

def delete_person_click():
    try:
        index = known_persons_lbox.curselection()[0]
    except IndexError:
        state.set('Выберите удаляемую персону')
    else:
        wanted = known_persons_lbox.get(index, index)[0]
        management.delete_person(wanted)
        known_persons_lbox.delete(index)
        state.set(f'Персона {wanted} удалена')

def focus_btn(event):
    event.widget['bg'] = 'gray50'

def defocus_btn(event):
    event.widget['bg'] = 'gray30'

lmain = Label()
lmain.place(relx=.04, rely=.1)

fps_label = Label(font='Arial 10',
                  width=6,
                  bg='gray80',
                  textvariable=fps_str)
fps_label.place(relx=.58, rely=.11)

known_persons_label = Label(text='Известные персоны:',
                      font='Arial 14',
                      width='30',
                      bg='gray30',
                      fg='gray80')
known_persons_label.place(relx=.65, rely=.1)

known_persons_lbox = Listbox(width=30,
                             height=17,
                             font='Arial 14',
                             bg='gray30',
                             fg='gray80',
                             selectbackground='brown1')
known_persons_lbox.place(relx=.65, rely=.15)

delete_person_btn = Button(text='Удалить персону',
                         font='Arial 14',
                         width='29',
                         relief='ridge',
                         bg='gray30',
                         fg='gray80',
                         activebackground='gray50',
                         command=delete_person_click)
delete_person_btn.place(relx=.65, rely=.71)
delete_person_btn.bind('<Enter>', focus_btn)
delete_person_btn.bind('<Leave>', defocus_btn)

new_person_label = Label(text='Имя новой персоны:',
                      font='Arial 14',
                      width='29',
                      bg='gray30',
                      fg='gray80')
new_person_label.place(relx=.04, rely=.8)

name_entry = Entry(font='Arial 14',
                   width='27',
                   bg='gray80',
                   fg='gray20',
                   textvariable=name)
name_entry.place(relx=.35, rely=.8)

add_person_btn =  Button(text='Добавить персону',
                         font='Arial 14',
                         width='29',
                         relief='ridge',
                         bg='gray30',
                         fg='gray80',
                         activebackground ='gray50',
                         command=add_person_click)
add_person_btn.place(relx=.04, rely=.85)
add_person_btn.bind('<Enter>', focus_btn)
add_person_btn.bind('<Leave>', defocus_btn)

add_person_file_btn =  Button(text='Добавить из файла',
                         font='Arial 14',
                         width='27',
                         relief='ridge',
                         bg='gray30',
                         fg='gray80',
                         activebackground='gray50',
                         command=add_person_file_click)
add_person_file_btn.place(relx=.35, rely=.85)
add_person_file_btn.bind('<Enter>', focus_btn)
add_person_file_btn.bind('<Leave>', defocus_btn)

state_label = Label(font='Arial 14',
                        width='29',
                        height='3',
                        bg='brown1',
                        fg='gray80',
                        textvariable=state)
state_label.place(relx=.65, rely=.8)

fill_listbox()
t = time.time()
show_frame()
window.mainloop()
