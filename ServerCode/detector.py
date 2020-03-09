import face_recognition
import cv2
import numpy as np
import json

def find_faces(frame):
    # нахождение только лиц,
    # принимает изображение,
    # возвращает изображение с выделенными лицами

    #frame = cv2.flip(frame, 1)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ratio = 480 / np.max(frame.shape)
    small_frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
    for (top, right, bottom, left) in face_locations:
        top = int(top / ratio)
        right = int(right / ratio)
        bottom = int(bottom / ratio)
        left = int(left / ratio)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), int(2 / ratio))
    return frame

def find_persons(frame):
    # нахождение сохраненных лиц,
    # принимает изображение,
    # возвращает изображение с подписанными лицами

    face_names = []
    with open('persons.json') as persons:
        data = json.load(persons)
        known_face_encodings = data['encodings']
        known_face_names = data['names']
    # frame = cv2.flip(frame, 1)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ratio = 480 / np.max(frame.shape)
    small_frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        name = "Unknown"
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top = int(top / ratio)
        right = int(right / ratio)
        bottom = int(bottom / ratio)
        left = int(left / ratio)
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), int(1 / ratio))
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return frame


# f = find_faces(cv2.imread('lohs.jpg'))
# cv2.imshow('Detected', f)
# cv2.waitKey()

# f = find_persons(cv2.imread('lohs.jpg'))
# cv2.imshow('Detected', f)
# cv2.waitKey()
