import cv2
import numpy as np
from possible import Possible

img_input = "images/error1_1.jpg"


# args is images thresh
def rotation_rect(thresh):
    # coords
    coords = np.column_stack(np.where(thresh == 0))
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = thresh.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def find_contours(thresh):
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    height, width = thresh.shape
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    for i in range(0, len(contours)):
        possible = Possible(contours[i])
        h = possible.bounding_react_height
        w = possible.bounding_react_with
        x = possible.bounding_react_x
        y = possible.bounding_react_y
        roi = img_contours[y:y+h, x:x+w]
        cv2.imwrite("output/" + str(i)+".png", roi)
    print("Len contours:", str(len(contours)))
    return img_contours


def main():
    print("=== Detect Cracks Of Object ===")
    img = cv2.imread(img_input)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imshow("thresh",  thresh)

    img_contours = find_contours(thresh)
    # cv2.imshow("img contours", img_contours)
    cv2.imwrite("output/img_contours.png", img_contours)

    # # rotationed images
    # rotationed = rotation_rect(thresh)
    # cv2.imwrite("images/rotated.png", rotationed)
    # cv2.waitKey(0)
    print("=== Done ===")


if __name__ == "__main__":
    main()
