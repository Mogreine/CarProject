from tkinter import *
import cv2
from PIL import Image, ImageTk
import json
import detector
import management

window = Tk()
window.title('Здарова, блет')
window.geometry('1080x720+300+100')
window.configure(bg='Light Blue')

imageFrame = Frame(window, width=1000, height=500)
#imageFrame.grid(row=0, column=0, padx=10, pady=10)

name = StringVar()
video_capture = cv2.VideoCapture(0)

def show_frame():
    frame = video_capture.read()[1]
    frame = cv2.flip(frame, 1)
    cv2image = detector.find_persons(frame)
    cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def fill_listbox():
    with open('persons.json') as persons:
        data = json.load(persons)
        for i in data['names']:
            known_persons_lbox.insert(END, i)

def add_person_click():
    frame = video_capture.read()[1]
    frame = cv2.flip(frame, 1)
    management.add_person(name.get(), frame)
    known_persons_lbox.insert(END, name.get())

def delete_person_click():
    index = known_persons_lbox.curselection()[0]
    wanted = known_persons_lbox.get(index, index)[0]
    management.delete_person(wanted)
    known_persons_lbox.delete(index)

lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
imageFrame.place(relx=.04, rely=.1)

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
                   width='28',
                   textvariable=name)
name_entry.place(relx=.35, rely=.8)

add_person_btn =  Button(text='Добавить персону',
                         font='Arial 14',
                         width='58',
                         relief='groove',
                         bg='Deep Sky Blue',
                         highlightcolor='SteelBlue1',
                         command=add_person_click)
add_person_btn.place(relx=.04, rely=.85)

fill_listbox()
show_frame()
window.mainloop()