import cv2
import numpy as np

img1 = cv2.imread("image/road.jpg")
img2 = cv2.imread("image/car.jpg")

sum_img = cv2.add(img1, img2)
# add weight from 0 to 1
weighted = cv2.addWeighted(img1, 0.3, img2, 0.7, 0)
cv2.imwrite("image/05.weighted.png", weighted)

cv2.imwrite("image/sum_img.png", sum_img)
