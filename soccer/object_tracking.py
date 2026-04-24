import cv2
import numpy as np
# import serial


video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()
tracker = cv2.legacy.MultiTracker_create()

boxes = []
boxes.append(cv2.selectROI('select', frame, False))
boxes.append(cv2.selectROI('select', frame, False))

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
    cv2.imshow('gfg', img3)

    # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # rgb_small_frame = small_frame[:, :, ::-1]


    # if ret:

    #     x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    #     cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    #     cv2.putText(frame, "Tracking Target", (75, 75), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
    # else:
    #     cv2.putText(frame, "Target Lost", (75, 75), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)



    # for (top, right, bottom, left), name in zip(face_locations, face_names):

    #     top *= 2
    #     right *= 2
    #     bottom *= 2
    #     left *= 2

    #     cv2.rectangle(frame, (left + 10, top + 80), (right - 10, bottom), (0, 0, 255), 2)

    #     cv2.rectangle(frame, (left + 20, bottom), (right - 20, bottom), (0, 0, 255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 10, bottom - 6), font, 0.55, (50, 50, 50), 1)

       

    cv2.imshow('Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

video_capture.release()
cv2.destroyAllWindows()