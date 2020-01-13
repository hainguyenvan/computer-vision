import cv2
import numpy as np

cap = cv2.VideoCapture("/home/user1/Project/casper/face/video2.mp4")

while True:
    ret, frame = cap.read()
    thresh = 40
    min_bgr = np.array([frame[0]])

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
