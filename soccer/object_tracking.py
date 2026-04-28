import cv2
import numpy as np
import serial

ser = serial.Serial('/dev/tty.usbmodem101')

video_capture = cv2.VideoCapture(0)
tracker = cv2.TrackerCSRT_create()

ret, frame = video_capture.read()
bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)


def ShiftR():
    print("testr")
    print(ser.name)
    ser.write(b'1')
    print("testwrite1")
    data = ser.readline().decode('ascii')
    return data

def ShiftL():
    print("testl")
    print(ser.name)
    ser.write(b'2')
    print("testwrite2")
    data = ser.readline().decode('ascii')
    return data



while (1):

    ret, frame = video_capture.read()
    ret, bbox = tracker.update(frame)

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    rgb_small_frame = small_frame[:, :, ::-1]


    if ret:

        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
        cv2.putText(frame, "Tracking Target", (75, 75), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Target Lost", (75, 75), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)

    print(bbox[0])
  
    # if img2x > img3x:
    #     print ("move Right by")
    #     ShiftR()

    # elif img3x < img2x:
    #     print ("move left by")
    #     ShiftL()

            
    cv2.imshow('Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

video_capture.release()
cv2.destroyAllWindows()