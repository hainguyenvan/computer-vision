import cv2
import numpy as np

img1 = cv2.imread("image/drawing_1.png")
img2 = cv2.imread("image/drawing_2.png")

# bitwise and
bit_and = cv2.bitwise_and(img1, img2)
cv2.imwrite("image/07.bit_and.png", bit_and)

# bitwise or
bit_or = cv2.bitwise_or(img1, img2)
cv2.imwrite("image/07.bit_or.png", bit_or)

# bitwise xor
bit_xor = cv2.bitwise_xor(img1, img2)
cv2.imwrite("image/07.bit_xor.png", bit_xor)

# bit not of image 1
bit_not_1 = cv2.bitwise_not(img1)
cv2.imwrite("image/07.bit_not_1.png", bit_not_1)

# bit not of image 2
bit_not_2 = cv2.bitwise_not(img2)
cv2.imwrite("image/07.bit_not_2.png", bit_not_2)
