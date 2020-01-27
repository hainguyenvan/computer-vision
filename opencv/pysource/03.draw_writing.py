import cv2
import numpy as np

img = cv2.imread("image/good.jpg")
# get size of image
shape = img.shape

# define color
bule = (255, 0, 0)
red = (0, 0,  255)
green = (0, 255, 0)
violet = (180, 0, 180)
yellow = (0, 180, 180)
white = (255, 255, 255)

# draw on the image in order: a line, a circle, a rectangle,
# an ellipse and a polygon
# draw line
cv2.line(img, (50, 30), (450, 35), bule, thickness=5)
# draw circle
cv2.circle(img, (240, 205), 23, red, -1)
# draw rectangle
cv2.rectangle(img, (50, 60), (450, 95), green, -1)
# draw ellipse
cv2.ellipse(img, (250, 150), (80, 20), 5, 0, 360, violet, -1)
# polylines
points = np.array([[[140, 230], [380, 230], [320, 250], [250, 280]]], np.int32)
cv2.polylines(img, [points], True, yellow, thickness=3)

# draw text
font = cv2.FONT_HERSHEY_COMPLEX
cv2.putText(img, "Pro master", (20, 180), font, 2, white)

cv2.imwrite("image/03.draw_writing.png", img)
cv2.destroyAllWindows()
