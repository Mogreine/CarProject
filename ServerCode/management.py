import face_recognition
import cv2
import numpy as np
import json

def add_person(name, frame):
    #сохранение персоны в json

    ratio = 480 / np.max(frame.shape)
    frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
    exist = 0
    try:
        frame_encoding = face_recognition.face_encodings(frame)[0].tolist()
    except IndexError:
        return 2
    with open('persons.json') as persons:
        data = json.load(persons)
        try:
            i = data['names'].index(name)
        except ValueError:
            data['encodings'].append(frame_encoding)
            data['names'].append(name)
        else:
            data['encodings'][i] = frame_encoding
            data['names'][i] = name
            exist = 1
    with open('persons.json', 'w') as persons:
        json.dump(data, persons)
    return exist

def delete_person(name):
    #удаление персоны из json

    with open('persons.json') as persons:
        data = json.load(persons)
        try:
            i = data['names'].index(name)
        except ValueError:
            print('Person not found.')
        else:
            del data['encodings'][i]
            del data['names'][i]
    with open('persons.json', 'w') as persons:
        json.dump(data, persons)

# add_person('fucking_tatarin', cv2.imread('kamil.jpg'))
# add_person('sphere', cv2.imread('andre.jpg'))
# add_person('rat', cv2.imread('token.png'))

# delete_person('fucking_tatarin')
