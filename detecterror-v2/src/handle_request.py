import cv2
from skimage.measure import compare_ssim
import numpy as np

from translations import (highlight_contours, background_subtraction,
                          rotation_react_90, find_contours, resize_image, convert_image_to_thresh, crop_image_by_max_area)
from detects import is_error1, is_error2
from possible import Possible


def handle_background(img):
    thresh = convert_image_to_thresh(img)
    cv2.imwrite("pattern/background.jpg", thresh)
    return thresh


def handle_example_image(img):
    # convert image to thresh
    img = convert_image_to_thresh(img)
    img_background = cv2.imread("pattern/background.jpg")
    img_background = convert_image_to_thresh(img_background)

    # remove backgournd
    resized_img = resize_image(img_background, img)
    diff = resized_img - img_background

    contours, hierarchy = cv2.findContours(
        diff, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    max_area = -1
    index_max_area = -1
    possibles = []
    for i in range(0, len(contours)):
        possible = Possible(contours[i])
        possibles.append(possible)
        if max_area < possible.bounding_react_area:
            index_max_area = i
            max_area = possible.bounding_react_area

    # find contours possible
    possible_contours = []
    possible_max_area = possibles[index_max_area]
    x_min = possible_max_area.bounding_react_x
    y_min = possible_max_area.bounding_react_y
    x_max = x_min + possible_max_area.bounding_react_with
    y_max = y_min + possible_max_area.bounding_react_height
    for possible in possibles:
        x = possible.bounding_react_x
        y = possible.bounding_react_y
        if x >= x_min and x <= x_max and y >= y_min and y <= y_max:
            possible_contours.append(possible.contour)

    height = diff.shape[0]
    width = diff.shape[1]
    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.drawContours(img_contours, possible_contours, -1, [0, 255, 0], 2)
    cv2.imwrite("output/draw_contours.png", img_contours)

    # img_contours = convert_image_to_thresh(img_contours)
    # crop_image = crop_image_by_max_area(img_contours)

    return diff


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
