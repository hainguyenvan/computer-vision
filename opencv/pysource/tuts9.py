import cv2
import numpy as np


def nothing(x):
    print("x: ", str(x))
    pass


def nothing_lh(x):
    print("L-H: ", str(x))


def nothing_ls(x):
    print("L-X: ", str(x))


def nothing_lv(x):
    print("L-V: ", str(x))


def nothing_uh(x):
    print("U-H: ", str(x))


def nothing_us(x):
    print("U-S: ", str(x))


def nothing_uv(x):
    print("U-V: ", str(x))


cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L-H", "Trackbars", 0, 179, nothing_lh)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing_ls)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing_lv)
cv2.createTrackbar("U-H", "Trackbars", 179, 179, nothing_uh)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing_us)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing_uv)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s,  u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
