import cv2

from handle_request import handle_example_image

img = cv2.imread("input/good.jpg")
gray = handle_example_image(img)
cv2.imwrite("output/examples.png",  gray)
