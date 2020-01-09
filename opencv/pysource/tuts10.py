import cv2
import numpy as np

img = cv2.imread("error.JPG", cv2.IMREAD_GRAYSCALE)
_, threshold_binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
_, threshold_binary_inv = cv2.threshold(img, 128, 255,  cv2.THRESH_BINARY_INV)
_, threshold_trunc = cv2.threshold(img, 128, 255, cv2.THRESH_TRUNC)
_, threshold_to_zero = cv2.threshold(img, 12, 255, cv2.THRESH_TOZERO)

# cv2.imwrite("error_gray.png", img)
cv2.imshow("gray scale", img)
cv2.imshow("threshold binary", threshold_binary)
cv2.imshow("threshold trunc", threshold_trunc)
cv2.imshow("threshold to zero", threshold_to_zero)
cv2.waitKey(0)
cv2.destroyAllWindows()
