import cv2
import imutils

input = "good.jpg"
img = cv2.imread(input)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hue, saturation, value = cv2.split(hsv)
blur = cv2.GaussianBlur(value, (3, 3), 0)
thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2)

# find contours
contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# remove bad contours
cnts = imutils.grab_contours(cnts)
mask = np.ones(image.shape[:2], dtype="uint8") * 255


cv2.imwrite("save.png", thresh)
