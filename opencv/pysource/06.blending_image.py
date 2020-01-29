# import packages
import cv2
import numpy as np

img1 = cv2.imread("image/road.jpg")
img2 = cv2.imread("image/car.jpg")

# convert image to gray
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2_gray, 240, 255, cv2.THRESH_BINARY)
cv2.imwrite("image/06.mask.png", mask)

mask_inv = cv2.bitwise_not(mask)

road = cv2.bitwise_and(img1, img1, mask=mask)
cv2.imwrite("image/06.road_mask.png", road)
car = cv2.bitwise_and(img2, img2, mask=mask_inv)
cv2.imwrite("image/06.car_mask.png", car)
result = cv2.add(road, car)
cv2.imwrite("image/06.result_add.png", result)
