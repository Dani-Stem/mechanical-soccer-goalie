import face_recognition
import cv2
import numpy as np
import serial

ser = serial.Serial('/dev/ttyACM0')


def ShiftR():
    print(ser.name)
    ser.write(b'1')
    data = ser.readline().decode('ascii')
    return data

def ShiftL():
    print(ser.name)
    ser.write(b'2')
    data = ser.readline().decode('ascii')
    return data

def ShiftU():
    print(ser.name)
    ser.write(b'3') 
    data = ser.readline().decode('ascii')
    return data

def ShiftD():
    print(ser.name)
    ser.write(b'4')
    data = ser.readline().decode('ascii')
    return data

video_capture = cv2.VideoCapture(0)

tracker = cv2.TrackerCSRT_create()

pic1_image = face_recognition.load_image_file("dani0.jpg")
pic1_face_encoding = face_recognition.face_encodings(pic1_image)[0]

pic2_image = face_recognition.load_image_file("dani1.jpg")
pic2_face_encoding = face_recognition.face_encodings(pic2_image, None, 1, 'small')[0]

pic3_image = face_recognition.load_image_file("dani2.jpg")
pic3_face_encoding = face_recognition.face_encodings(pic3_image)[0]

known_face_encodings = [
    pic1_face_encoding,
    pic2_face_encoding,
    pic3_face_encoding
]
known_face_names = [
    "pic1",
    "pic2",
    "pic3"
]


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

i = 0

ret, frame = video_capture.read()
bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)

while True:

    ret, frame = video_capture.read()
    ret, bbox = tracker.update(frame)

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    rgb_small_frame = small_frame[:, :, ::-1]

    i = i + 1

    if i % 3 == 0:
        i = 0

        face_locations = face_recognition.face_locations(rgb_small_frame)
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

    if ret:

        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
        cv2.putText(frame, "Tracking Target", (75, 75), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Target Lost", (75, 75), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)



    for (top, right, bottom, left), name in zip(face_locations, face_names):

        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(frame, (left + 10, top + 80), (right - 10, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left + 20, bottom), (right - 20, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 10, bottom - 6), font, 0.55, (50, 50, 50), 1)

        if y > bottom:
            move_up = y - bottom
            print ("move up by", move_up)
            print(ShiftU())
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "too far DOWN", (left - 20, bottom + 20), font, 0.65, (0, 0, 255), 2)
        elif y < top:
            move_down = y - top
            print ("move down by", move_down)
            print(ShiftD())
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "too far UP", (left - 20, bottom + 20), font, 0.65, (0, 0, 255), 2)
        elif x > left:
            move_right = x - left
            print ("move Right by", move_right)
            print(ShiftR())
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "too far LEFT", (left - 20, bottom + 20), font, 0.65, (0, 0, 255), 2)
        elif x < right:
            move_left = x - right
            print ("move left by", move_left)
            print(ShiftL())
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "too far RIGHT", (left - 20, bottom + 20), font, 0.65, (0, 0, 255), 2)
        

    cv2.imshow('Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

video_capture.release()
cv2.destroyAllWindows()

