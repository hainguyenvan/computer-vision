import cv2
import numpy as np

img = cv2.imread("error.JPG")
rows, cols, ch = img.shape
print("rows: ", str(rows))
print("cols: ", str(cols))
print("channel: ", str(ch))
roi = img[100:280, 150:320]
img[250, 180] = (255, 0, 0)
cv2.imshow("image", img)
cv2.imshow("roi", roi)
cv2.waitKey(0)
cv2.distroyAllWindows()
