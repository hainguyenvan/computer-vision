import cv2

from handle_request import handle_background

img = cv2.imread("input/background.jpg")
gray = handle_background(img)
cv2.imwrite("output/background.jpg", gray)
