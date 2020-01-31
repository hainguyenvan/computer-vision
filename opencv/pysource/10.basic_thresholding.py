import cv2
import numpy as np


def notthing(x):
    pass


img = cv2.imread("image/red_panda.jpg", cv2.IMREAD_GRAYSCALE)
cv2.namedWindow("image")
cv2.createTrackbar("threshold value", "image", 128, 255, notthing)

while True:
    value_threshold = cv2.getTrackbarPos("threshold value", "image")
    _, threshold_binary = cv2.threshold(
        img, value_threshold, 255, cv2.THRESH_BINARY)
    _, threshold_binary_inv = cv2.threshold(
        img, value_threshold, 255, cv2.THRESH_BINARY_INV)
    _, threshold_trunc = cv2.threshold(
        img, value_threshold, 255, cv2.THRESH_TRUNC)
    _, threshold_to_zero = cv2.threshold(
        img, value_threshold, 255, cv2.THRESH_TOZERO)
    _, threshold_to_zero_inv = cv2.threshold(
        img, value_threshold, 255, cv2.THRESH_TOZERO_INV)

    # show image
    cv2.imshow("image", img)
    cv2.imshow("th binary", threshold_binary)
    cv2.imshow("th binary inv", threshold_binary_inv)
    cv2.imshow("th trunc", threshold_trunc)
    cv2.imshow("th to zero", threshold_to_zero)
    cv2.imshow("th to zero inv", threshold_to_zero_inv)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
