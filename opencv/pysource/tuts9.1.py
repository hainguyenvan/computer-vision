import cv2
import numpy as np

l_h = 35
l_s = 0
l_v = 0
u_h = 179
u_s = 255
u_v = 103

cap = cv2.VideoCapture("/home/user1/Project/casper/face/video2.mp4")

while True:
    ret, frame = cap.read()
    frame2 = cv2.flip(frame, 1)

    # hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([l_h,  l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    # end hsv

    cv2.imshow("frame", frame)
    cv2.imshow("frame result mask", result)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
