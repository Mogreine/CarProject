import face_recognition
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

video_capture = cv2.VideoCapture(0)
azat_image = face_recognition.load_image_file("example.jpg")
ratio = 480 / np.max(azat_image.shape)
azat_image = cv2.resize(azat_image, (0, 0), fx=ratio, fy=ratio)
azat_face_encoding = face_recognition.face_encodings(azat_image)[0]

known_face_encodings = [
    azat_face_encoding
]

known_face_names = [
    "Azatalion"
]

face_locations = []
face_encodings = []
face_names = []
times = []
frames = []
process_this_frame = True
num_frames = 480;
end = 0
start = time.time()
for i in range(num_frames):
    t0 = time.time()
    if i % 8 == 0:
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        # save = frame[:, :, ::-1]
        # cv2.imwrite('example.jpg', save)
        small_frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
        rgb_small_frame = small_frame[:, :, ::-1]
        #fps = video_capture.get(cv2.CAP_PROP_FPS)
        if process_this_frame:
            #print('?')
            face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

            #process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                #print('!')
                top = int(top / ratio)
                right = int(right / ratio)
                bottom = int(bottom / ratio)
                left = int(left / ratio)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow(f"Detected - {len(face_names)}", frame)
            print(i)
            cv2.waitKey(delay=1)
    times.append(time.time() - t0)
    frames.append(i)
end = time.time()
fps = num_frames / (end - start)
print(f"Time start - {start}, \nTime end - {end}, \nTime - {end - start}, \nFPS - {fps}")

plt.plot(frames, times)
plt.ylabel('time')
plt.xlabel('frame')
plt.show()

video_capture.release()
cv2.destroyAllWindows()

# image = face_recognition.load_image_file("II.jpg")
# ratio = 480 / np.max(image.shape)
# im = cv2.resize(image, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)
# face_locations = face_recognition.face_locations(im, model="cnn")
# face_locations = list(map(int, [face_locations[0][0] / ratio, face_locations[0][1] / ratio, face_locations[0][2] / ratio, face_locations[0][3] / ratio]))
# print(face_locations)
# cv2.rectangle(image, (face_locations[0], face_locations[1]), (face_locations[2], face_locations[3]), (255, 255, 0), 9)
# plt.imshow(image)
# plt.show()
