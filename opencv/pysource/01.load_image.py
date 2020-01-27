import cv2

# read image
img = cv2.imread("image/good.jpg")

# convert image to gray scale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# save img
cv2.imwrite("image/01.gray_img.png", gray_img)

# show img
cv2.imshow("gray img", gray_img)
cv2.imshow("rgb img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
