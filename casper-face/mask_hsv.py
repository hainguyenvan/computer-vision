import numpy as np
import cv2

l_h = 35
l_s = 0
l_v = 0
u_h = 179
u_s = 255
u_v = 103

output = "/home/user1/Project/casper/face/image1"
cap = cv2.VideoCapture("/home/user1/Project/casper/face/video1.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()

i = 0
while(1):
    ret, frame = cap.read()

    # convert to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s,  u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('hsv mask', result)
    cv2.imwrite(output+'/'+str(i)+".png", result)
    i = i+1

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
