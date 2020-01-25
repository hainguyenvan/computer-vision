import pickle
import cv2
import os

from .possible import (Possible, PossibleList)
from .utils import (
    rotation_rect, convert_image_to_thresh, find_contours)


# input: Image
# output: PossibleList
def save_samples(img):
    # get root dir
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

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

    cv2.imwrite(ROOT_DIR+"/output/thresh_img_example.png", thresh)
    cv2.imwrite(ROOT_DIR+"/output/rotationed_img_example.png", rotationed)

    # crop sample image
    # Find contour and sort by contour area
    _, cnts, _ = cv2.findContours(
        rotationed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # Find bounding box and extract ROI
    crop_sample_img = None
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        crop_sample_img = rotationed[y: y+h, x:x+w]
        break
    cv2.imwrite(ROOT_DIR+"/output/sample_crop_img.png", crop_sample_img)

    # find contours
    img_contours, possibles, max_area_possible = find_contours(crop_sample_img)
    cv2.imwrite(ROOT_DIR+"output/contours_img_example.png", img_contours)

    example_possibles = PossibleList(possibles, max_area_possible)
    with open(ROOT_DIR+"/samples/possible_samples.dictionary", "wb") as config_dictionary_file:
        pickle.dump(example_possibles, config_dictionary_file)

    return example_possibles


# get samples
def get_samples():
    # get root dir
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    possible_samples = None
    with open(ROOT_DIR+"/samples/possible_samples.dictionary", "rb") as config_dictionary_file:
        possible_samples = pickle.load(config_dictionary_file)

    return possible_samples
