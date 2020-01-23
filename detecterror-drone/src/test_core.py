import numpy as np
import cv2

from core.utils import(rotation_rect)
from core.samples import (save_samples)


def test_rotation_rect():
    print("[INFO] Test rotation rect")
    img = cv2.imread("input/good.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    _, contours, _ = cv2.findContours(edge.copy(), 1, 1)
    # contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    rotation_img = rotation_rect(thresh)
    cv2.imwrite("output/rotation_img.png", rotation_img)
    print("[INFO] Done")


def test_save_samples():
    print("[INFO] Test save samples")
    img = cv2.imread("input/good.jpg")
    save_samples(img)
    print("[INFO] Done")


# test_rotation_rect()
test_save_samples()
