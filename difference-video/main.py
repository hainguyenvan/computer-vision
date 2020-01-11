import cv2
import imutils
import numpy as np

import functions


input_video = "video1.mp4"
output_frame = "/home/rombk/Project/images-processing/101/frame-image"

cap = cv2.VideoCapture(input_video)
_, first_frame = cap.read()
gray_first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
gray_first_frame = cv2.GaussianBlur(gray_first_frame, (5, 5), 0)

index = 0
while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    diff = cv2.absdiff(gray_first_frame, gray_frame)
    _, diff = cv2.threshold(diff, 2, 255, cv2.THRESH_BINARY)

    # get counter
    cnts = cv2.findContours(
        diff, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    height, width = diff.shape
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    possibles = []
    for i in range(0, len(cnts)):
        possible = functions.Possible(cnts[i])
        is_lower_px = functions.is_possible(possible, 500, 4)
        if is_lower_px:
            possibles.append(possible)
    ctrs_possibles = []
    for possible in possibles:
        ctrs_possibles.append(possible.contour)
    result = cv2.drawContours(
        img_contours, ctrs_possibles, -1, (255, 255, 255))
    gray_first_frame = gray_frame

    print("Len cnts: ", str(len(cnts)))
    cv2.imshow("result: ", result)
    cv2.imshow("diff", diff)
    cv2.imshow("gray first frame", gray_first_frame)
    cv2.imshow("frame", frame)

    img_frame = output_frame+"/"+str(index)+".png"
    cv2.imwrite(img_frame, frame)
    index += 1
    # quit
    key = cv2.waitKey(33)
    if key == 27:
        break

cap.release()
cv2.distroyAllWindows()
