import cv2
import numpy as np

from translations import resize_image, find_contours, highlight_contours
from possible import Possible

# error1: loss circle


def is_error1(possibles):
    if len(possibles) == 8:
        return False
    return True


# error2: translate circle
def is_error2(img):
    img_pattern = cv2.imread("pattern/example.png")
    # resize images
    img = resize_image(img_pattern, img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue, saturation, value = cv2.split(hsv)
    # cv2.imwrite("output/hsv.png", value)

    # find contours
    # gray_pattern = cv2.cvtColor(img_pattern, cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(
        value, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    height, width = value.shape
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    for i in range(0, len(contours)):
        possible = Possible(contours[i])
        h = possible.bounding_react_height
        w = possible.bounding_react_with
        x = possible.bounding_react_x
        y = possible.bounding_react_y
        roi = img_contours[y:y+h, x:x+w]
        possible.roi = roi
        # possibles.append(possible)
        cv2.imwrite("output/roi" + str(i)+".png", roi)
    # _, pattern_possibles, _ = find_contours(value)
    print(str(len(contours)))
    # thresh_pattern = highlight_contours(gray_pattern)

    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresh_img = highlight_contours(gray_img)

    # pattern_possibles = find_contours(thresh_pattern)
    # img_possibles = find_contours(thresh_img)

    # for i in range(0, len(pattern_possibles)):
    #     cv2.imwrite("output/error2" + str(i)+".png", pattern_possibles[i].roi)
    # print("Len pattern: ", str(len(pattern_possibles)))
    # print("Len img: ", str(len(img_possibles)))
    # def get_contour_possibles(img):
    #     print("Hello ============")
    # find_contours(img)
    # _, pattern_possibles, _ = find_contours(img_pattern)
    # _, img_possibles, _ = find_contours(img)
    # print("Len pattern: ", str(len(pattern_possibles)))
    # print("Len img: ", str(len(img_possibles)))
    # cv2.imwrite("output/resize.png",  img)
    return True
