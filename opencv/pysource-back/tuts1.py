import cv2

input_image = "error.JPG"
img = cv2.imread(input_image)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# show image
# cv2.imshow("Gray image", gray_img)
# cv2.imshow("Red image", img)
cv2.imwrite("gray.png", gray_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
