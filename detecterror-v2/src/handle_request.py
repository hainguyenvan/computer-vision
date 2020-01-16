import cv2
import pickle
import numpy as np

from translations import highlight_contours, background_subtraction, rotation_react_90, find_contours
from detects import is_error1, is_error2


def handle_background(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    background = highlight_contours(gray)
    # cv2.imwrite("input/background.png", background)
    return background


def handle_example_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = highlight_contours(gray)
    rotation_img = rotation_react_90(thresh)
    # background_img = cv2.imread("input/background.png")
    # diff = background_subtraction(background_img, gray)
    rotation_img = highlight_contours(rotation_img)
    contour_img, possibles, index_max_area = find_contours(rotation_img)
    cv2.imwrite("pattern/example.png", possibles[index_max_area].roi)

    # dumpy objects
    pickle_out = open("pattern/example.pickle", "wb")
    pickle.dump(possibles, pickle_out)
    pickle_out.close()
    return possibles[index_max_area].roi


def handle_detect(img):
    # step1: background subtraction
    # convert images to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = highlight_contours(gray)
    # background_img = cv2.imread("input/background.png")
    # diff = background_subtraction(background_img, gray)

    # step2: rotation image
    rotation_img = rotation_react_90(thresh)
    rotation_img = highlight_contours(rotation_img)
    contour_img, possibles, index_max_area = find_contours(rotation_img)

    # step3: check error1
    error1 = is_error1(possibles)
    if error1:
        retusult = {
            "type": "error1"
        }
        return retusult

    # step4: check error2
    max_area = possibles[index_max_area]
    error2 = is_error2(max_area.roi)
    cv2.imwrite("output/max_area.png", max_area.roi)
    # cv2.imwrite("output/contour_img.png", contour_img)
    return None
