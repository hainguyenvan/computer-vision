import cv2
import imutils
from skimage.measure import compare_ssim

input_video = "video1.mp4"
output_frame = "/home/rombk/Project/images-processing/101/frame-image"

cap = cv2.VideoCapture(input_video)
subtractor = cv2.createBackgroundSubtractorMOG2(
    history=20, varThreshold=25, detectShadows=True)

index = 0
while True:
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    mask = subtractor.apply(gray_frame)

    cv2.imshow("mask",  mask)
    cv2.imshow("frame", frame)
    index += 1
    # quit
    key = cv2.waitKey(33)
    if key == 27:
        break

cap.release()
cv2.distroyAllWindows()
