import cv2

import functions

img = cv2.imread("good.JPG")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hue, saturation, value = cv2.split(hsv)
blur = cv2.GaussianBlur(value, (3, 3), 0)
thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2)

detect = functions.detect(thresh,  0)
print("detect: ", detect)
