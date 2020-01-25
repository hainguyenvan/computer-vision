# import packages
import numpy as np
import cv2
import os

from .utils import (convert_image_to_thresh, rotation_rect,
                    find_contours, resize_image)
from .detects_error1 import (detect_error1)
from .jaccard_similarity import (JaccardBox, jaccard_similarity)
from .samples import (get_samples)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def detect_error(img):
    thresh = convert_image_to_thresh(img)
    rotationed = rotation_rect(thresh)

    # highlight contours
    rotationed = cv2.GaussianBlur(rotationed, (11, 11), 0)
    edge = cv2.Canny(rotationed, 100, 200)
    _, contours, _ = cv2.findContours(edge.copy(), 1, 1)
    # contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(rotationed, contours, -1, [0, 255, 0], 2)
    rotationed = cv2.bitwise_not(rotationed)
    rotationed = cv2.threshold(
        rotationed, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite(ROOT_DIR+"/output/detects_rotation.png", rotationed)

    # Find contour and sort by contour area
    _, cnts, _ = cv2.findContours(
        rotationed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # Find bounding box and extract ROI
    crop_detects_img = None
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        crop_detects_img = rotationed[y: y+h, x:x+w]
        break
    cv2.imwrite(ROOT_DIR+"/output/crop_img.png", crop_detects_img)

    # load samples
    # create jaccard box
    jaccard_box_samples = []
    samples_possibles = get_samples()
    max_possible = samples_possibles.max_area_possible
    for i in range(0, len(samples_possibles.possibles)):
        # init x, y, width, height
        x = samples_possibles.possibles[i].bounding_react_x
        y = samples_possibles.possibles[i].bounding_react_y
        width = samples_possibles.possibles[i].bounding_react_with
        height = samples_possibles.possibles[i].bounding_react_height

        jaccard = JaccardBox(x, y, width, height)
        jaccard.possible = samples_possibles.possibles[i]
        jaccard_box_samples.append(jaccard)

    # find contours of detects
    width = max_possible.bounding_react_with
    height = max_possible.bounding_react_height
    all_possible = resize_image(width,  height, crop_detects_img)
    cv2.imwrite(ROOT_DIR+"/output/all_possible.png", all_possible)

    # check contours after resize image by image exmaples
    img_contours, detect_possibles, max_area_possible = find_contours(
        all_possible)
    cv2.imwrite(ROOT_DIR+"/output/detects_img.png", max_area_possible.roi)

    # create detects possible
    jaccard_box_detects = []
    for i in range(0, len(detect_possibles)):
        # init x, y, width, height
        x = detect_possibles[i].bounding_react_x
        y = detect_possibles[i].bounding_react_y
        width = detect_possibles[i].bounding_react_with
        height = detect_possibles[i].bounding_react_height

        jaccard = JaccardBox(x, y, width, height)
        jaccard.possible = detect_possibles[i]
        jaccard_box_detects.append(jaccard)

    # sort array by y
    sorted_jaccrad_samples = sorted(
        jaccard_box_samples, key=lambda item: item.area)
    sorted_jaccard_detects = sorted(
        jaccard_box_detects, key=lambda item: item.area)

    # check error1
    error1_possibles = detect_error1(
        sorted_jaccard_detects, sorted_jaccrad_samples)
    # draw error1
    for i in range(0, len(error1_possibles)):
        x_min = error1_possibles[i].x_min
        y_min = error1_possibles[i].y_min
        x_max = error1_possibles[i].x_max
        y_max = error1_possibles[i].y_max
        cv2.rectangle(img_contours, (x_min, y_min),
                      (x_max, y_max), (0, 0, 255), 2)
    cv2.imwrite(ROOT_DIR+"/output/result_detect_error.png", img_contours)
    # end check erorr1

    print("==============")
    print("Len error: ", str(len(error1_possibles)))
