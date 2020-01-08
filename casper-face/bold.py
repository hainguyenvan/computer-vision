from cv2 import cv2
import numpy as np

img = cv2.imread("image_200.jpg")
kernel = np.ones((5, 5), np.uint8)

# Bước 1: Chuyển về ảnh xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Bước 2: Làm mờ ảnh
blur = cv2.GaussianBlur(gray, (9, 9), 1)
cv2.imwrite("test200.png", blur)

# Bước 3: Lọc nhiễu
new = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, -5)

cv2.imwrite("test.png", new)
