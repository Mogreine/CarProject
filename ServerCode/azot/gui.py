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
window.configure(bg='Light Blue')

imageFrame = Frame(window, width=1080, height=720)
imageFrame.grid(row=0, column=0, padx=10, pady=10)

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
    if frames < 10:
        t = time.time()
    else:
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


lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
imageFrame.place(relx=.04, rely=.1)

fps_label = Label(font='Arial 10',
                  width=6,
                  bg='White',
                  textvariable=fps_str)
fps_label.place(relx=.58, rely=.11)

known_persons_label = Label(text='Известные персоны:',
                            font='Arial 14',
                            width='30',
                            bg='Azure')
known_persons_label.place(relx=.64, rely=.1)

known_persons_lbox = Listbox(width=30, height=17, font='Arial 14')
known_persons_lbox.place(relx=.64, rely=.15)

delete_person_btn = Button(text='Удалить персону',
                           font='Arial 14',
                           width='29',
                           relief='groove',
                           bg='Deep Sky Blue',
                           highlightcolor='SteelBlue1',
                           command=delete_person_click)
delete_person_btn.place(relx=.64, rely=.71)

new_person_label = Label(text='Имя новой персоны:',
                         font='Arial 14',
                         width='29',
                         bg='Azure')
new_person_label.place(relx=.04, rely=.8)

name_entry = Entry(font='Arial 14',
                   width='27',
                   textvariable=name)
name_entry.place(relx=.35, rely=.8)

add_person_btn = Button(text='Добавить персону',
                        font='Arial 14',
                        width='29',
                        relief='groove',
                        bg='Deep Sky Blue',
                        highlightcolor='SteelBlue1',
                        command=add_person_click)
add_person_btn.place(relx=.04, rely=.85)

add_person_file_btn = Button(text='Добавить из файла',
                             font='Arial 14',
                             width='27',
                             relief='groove',
                             bg='Deep Sky Blue',
                             highlightcolor='SteelBlue1',
                             command=add_person_file_click)
add_person_file_btn.place(relx=.35, rely=.85)

state_label = Label(font='Arial 14',
                    width='29',
                    height='3',
                    bg='Azure',
                    textvariable=state)
state_label.place(relx=.64, rely=.8)

fill_listbox()
t = time.time()
show_frame()
window.mainloop()
