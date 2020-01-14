import numpy as np
import cv2

print("=== Text Skew  Correction Examples ===")
img_path = "m20.jpg"
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# set background is  "black"
gray = cv2.bitwise_not(gray)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# cv2.imwrite("test.png", thresh)

# get (x,y) of pixel white
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
(h, w) = img.shape[:2]
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(
    img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
# cv2.imwrite("test2.png",)
print("[Info] angle: ", str(angle))
cv2.imshow("Image", img)
cv2.imshow("Rotated", rotated)
cv2.waitKey(0)
