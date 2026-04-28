import cv2
import numpy as np
import serial

ser = serial.Serial('/dev/tty.usbmodem101')

video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()
tracker = cv2.legacy.MultiTracker_create()

boxes = []
boxes.append(cv2.selectROI('select', frame, False))
boxes.append(cv2.selectROI('select', frame, False))



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


for box in boxes:
    tracker.add(cv2.legacy.TrackerCSRT_create(), frame, box)


while (1):

    ret, frame = video_capture.read()
    ret, boxes = tracker.update(frame)

    if ret:
        for box in boxes:
            x, y, w, h = (int(t) for t in box)
            img2 = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 2)
            img3 = cv2.rectangle(img2, (x, y), (x+w, y+h), 255, 2)
            img2coords = boxes[0]     
            img3coords = boxes[1]     
            img2x = img2coords[0]
            print(img2x)
            img3x = img3coords[0]
            print(img3x)


    cv2.imshow('gfg', img3)
  
    if img2x > img3x:
        print ("move Right by")
        ShiftR()

    elif img3x < img2x:
        print ("move left by")
        ShiftL()
            

    cv2.imshow('Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

video_capture.release()
cv2.destroyAllWindows()