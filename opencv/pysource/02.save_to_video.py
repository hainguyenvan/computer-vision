import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# config save video
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# 25: fps(frame per seconds)
out = cv2.VideoWriter("image/02.save_to_video.avi", fourcc, 25, (640, 360))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # 1: vertical flip by frame
    # 0: horizontal flip by frame
    frame_output = cv2.flip(frame, 0)
    cv2.imshow("input", frame)
    cv2.imshow("output", frame_output)

    # save output
    out.write(frame_output)

    # wait bread
    key = cv2.waitKey(1)
    if key == 27:
        break
# destroy
out.release()
cap.release()
cv2.destroyAllWindows()
