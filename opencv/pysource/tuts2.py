import cv2
import numpy as ns

# # read from webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     cv2.imshow("frame", frame)
#     key = cv2.waitKey(1)
#     if key == 27:
#         break

# cap.release()
# cv2.distroyAllWindows()


# read video from file and save it to file
fgbg = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture("red_panda_snow.mp4")
# save it to file avi
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("flipped_red_panda.avi", fourcc, 25, (640, 360))

while True:
    ret, frame = cap.read()
    frame2 = cv2.flip(frame, 1)
    cv2.imshow("frame1", frame)

    gray_img = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray_img)
    cv2.imshow("frame2", fgmask)
    out.write(fgmask)
    key = cv2.waitKey(25)
    if key == 27:
        break
out.release()
cap.release()
cv2.distroyAllWindows()
