import cv2
import numpy as np

from possible import Possible


def resize_image(img_pattern, img):
    height, width, channels = img_pattern.shape
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def highlight_contours(gray):
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edge.copy(), 1, 1)

    # highlight contours
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh


def find_contours(thresh):
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    height, width = thresh.shape
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
    possibles = []
    index_max_area = -1
    max_area = -1
    for i in range(0, len(contours)):
        possible = Possible(contours[i])
        h = possible.bounding_react_height
        w = possible.bounding_react_with
        x = possible.bounding_react_x
        y = possible.bounding_react_y
        roi = img_contours[y:y+h, x:x+w]
        possible.roi = roi
        possibles.append(possible)
        if max_area < possible.bounding_react_area:
            index_max_area = i
        cv2.imwrite("output/" + str(i)+".png", roi)
    # print("Len contours:", str(len(contours)))
    return img_contours, possibles, index_max_area

# def processing_images(img):
#         # convert to
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     return thresh


def background_subtraction(backround, img):
    diff = cv2.absdiff(backround, img)
    _, contours, hierarchy = cv2.findContours(
        diff, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    height, width = diff.shape
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 2)
    return diff


def rotation_react_90(thresh):
    # coords
    coords = np.column_stack(np.where(thresh == 0))
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    size = rect[1]
    height_rect, width_rect = size
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
