import cv2
import numpy as np

img = cv2.imread("image/red_panda.jpg")
height, width, ch = img.shape

print("Height: ",  height)
print("Width: ", width)

scaled_img = cv2.resize(img, None, fx=1/2, fy=1/2)

maxtrix_t = np.float32([[1, 0, -100], [0, 1, -30]])
translated_img = cv2.warpAffine(img, maxtrix_t, (width,  height))

maxtrix_r = cv2.getRotationMatrix2D((width/2,  height/2), 90, 0.5)
rotated_img = cv2.warpAffine(img, maxtrix_r,  (width, height))

cv2.imshow("Original image",  img)
cv2.imshow("Scaled image", scaled_img)
cv2.imshow("Translated image", translated_img)
cv2.imshow("Rotated image", rotated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
