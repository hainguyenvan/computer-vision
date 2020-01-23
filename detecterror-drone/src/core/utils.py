# import packages
import numpy as np
import cv2

from possible import Possible


# only input is thresh image
def rotation_rect(thresh_img):
    # coords
    coords = np.column_stack(np.where(thresh_img == 0))
    rect = cv2.minAreaRect(coords)

    angle = rect[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = thresh_img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        thresh_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# convert image to thresh
def convert_image_to_thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    _, contours, _ = cv2.findContours(edge.copy(), 1, 1)
    # contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh

# find countours
def find_contours(thresh):
    _, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contours, hierarchy = cv2.findContours(
    #     thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    height, width = thresh.shape
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    max_area_possible = -1
    item_max_area_possible = None
    possibles = []

    for i in range(0, len(contours)):
        possible = Possible(contours[i])
        # print("area:", str(possible.bounding_react_area))
        if possible.bounding_react_area > 20:
            h = possible.bounding_react_height
            w = possible.bounding_react_with
            x = possible.bounding_react_x
            y = possible.bounding_react_y
            roi = img_contours[y:y+h, x:x+w]
            possible.roi = roi
            if max_area_possible <= possible.bounding_react_area:
                max_area_possible = possible.bounding_react_area
                item_max_area_possible = possible
            possibles.append(possible)
            cv2.imwrite("output/" + str(i)+".png", roi)
    return img_contours, possibles, item_max_area_possible
