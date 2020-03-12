print('Загрузка модулей...')
try:
    import face_recognition
    print('Модель найдена.')
except Exception as e:
    print(str(e), '- Модель не найдена.')
import cv2
import numpy as np
import json
try:
    open('persons.json')
    print('JSON найден.')
except Exception as e:
    print(str(e), '- JSON не найден.')
from PIL import Image, ImageDraw, ImageFont
import dlib
if dlib.DLIB_USE_CUDA:
    print('GPU ускорение доступно (DLIB_USE_CUDA = True).')
else:
    print('GPU ускорение не доступно (DLIB_USE_CUDA = False).')
print('Все готово, чтобы писать историю.')

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
    ratio = 480 / np.max(frame.shape)
    small_frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        name = "Unknown"
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        try:
            best_match_index = np.argmin(face_distances)
        except Exception:
            name = "Unknown"
        else:
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):

        top = int(top / ratio)
        right = int(right / ratio)
        bottom = int(bottom / ratio)
        bottom += int(0.35 * (bottom - top))
        left = int(left / ratio)
        cv2.rectangle(frame, (left, top), (right, bottom), (205, 205, 205), int(2 / ratio))
        img = np.zeros((int(0.1 * (bottom - top)), right - left, 3), np.uint8)
        img[:,:] = [205, 205, 205]
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype('arial.ttf', int(0.1 * (bottom - top)))
        draw.text((0, 0), name, font=font, fill=(15, 15, 15, 0))
        try:
            frame[bottom - int(0.1 * (bottom - top)):min(bottom, frame.shape[0]), left:min(right, frame.shape[1])] = img_pil
        except Exception as e:
            print(str(e), '- не влезаем!')

        #cv2.imshow('f', np.array(img_pil))

    return frame


# f = find_faces(cv2.imread('lohs.jpg'))
# cv2.imshow('Detected', f)
# cv2.waitKey()

# f = find_persons(cv2.imread('lohs.jpg'))
# cv2.imshow('Detected', f)
# cv2.waitKey()
