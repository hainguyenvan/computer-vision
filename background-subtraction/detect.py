import numpy as np
import cv2

print("=== Detects Error Of Casper ===")
# load image
first_input = "image_001.jpg"
last_input = "image_002.jpg"
# first_input = "goodIMG_3258.JPG"
# last_input = "error.JPG"
first_img = cv2.imread(first_input)
last_img = cv2.imread(last_input)
tmp_img = cv2.imread(last_input)

print("Step 1: Convert images to HSV")
first_gray = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (21, 21), 0)
last_gray = cv2.cvtColor(last_img, cv2.COLOR_BGR2GRAY)
last_gray = cv2.GaussianBlur(last_gray, (21, 21), 0)
tmp_gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
tmp_gray = cv2.GaussianBlur(tmp_gray, (21, 21), 0)
cv2.imwrite("1.hsv_first.png", first_gray)
cv2.imwrite("1.hsv_last.png", last_gray)

print("Step 2: ")
difference = cv2.absdiff(last_gray, first_gray)
thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
cv2.imwrite("2.result.png", thresh)

difference = cv2.absdiff(difference, first_gray)
thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
cv2.imwrite("3.result.png", thresh)
