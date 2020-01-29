import cv2
import numpy as np


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow("frame")
cv2.createTrackbar("test", "frame", 50, 500, nothing)
cv2.createTrackbar("color/gray", "frame", 0, 1, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    test = cv2.getTrackbarPos("test", "frame")
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, str(test), (50, 150), font, 4, (0, 0, 255))

    s = cv2.getTrackbarPos("color/gray", "frame")
    if s == 0:
        pass
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
