import cv2
import numpy as np
import pickle
import base64

from possible import (Possible, PossibleList)


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

    # highlight contours
    gray = cv2.GaussianBlur(rotated, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    # _, contours, _ = cv2.findContours(edge.copy(), 1, 1)
    contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh


def convert_image_to_thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    # _, contours, _ = cv2.findContours(edge.copy(), 1, 1)
    contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh


def find_contours(thresh):
    # _, contours, hierarchy = cv2.findContours(
    #     thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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


def resize_image(width, height, img):
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def handle_image_examples(img):
    thresh = convert_image_to_thresh(img)
    rotationed = rotation_rect(thresh)
    cv2.imwrite("output/thresh_img_example.png", thresh)
    cv2.imwrite("output/rotationed_img_example.png", rotationed)
    img_contours, possibles, max_area_possible = find_contours(rotationed)
    cv2.imwrite("output/contours_img_example.png", img_contours)

    # save pattern
    cv2.imwrite("pattern/example.png", max_area_possible.roi)
    example_possibles = PossibleList(possibles, max_area_possible)
    with open('pattern/example.dictionary', 'wb') as config_dictionary_file:
        pickle.dump(example_possibles, config_dictionary_file)

    ret, buffer = cv2.imencode('.jpg', max_area_possible.roi)
    jpg_as_text = base64.b64encode(buffer)
    # print(jpg_as_text)
    return jpg_as_text


def handle_detect(img):
    thresh = convert_image_to_thresh(img)
    rotationed = rotation_rect(thresh)
    cv2.imwrite("output/thresh_img_detect.png", thresh)
    cv2.imwrite("output/rotationed_img_detect.png", rotationed)
    img_contours, possibles, max_area_possible = find_contours(rotationed)
    cv2.imwrite("output/contours_img_detect.png", img_contours)

    # load image examples
    example_possibles = None
    with open('pattern/example.dictionary', 'rb') as config_dictionary_file:
        example_possibles = pickle.load(config_dictionary_file)

    # get max area possible and resize image by examples
    max_possible = example_possibles.max_area_possible
    # convert image models to base64
    ret_examples, buffer_examples = cv2.imencode('.jpg', img_contours)
    jpg_as_text_examples = base64.b64encode(buffer_examples)

    # check loss circle
    if len(possibles) != 8:
        ret, buffer = cv2.imencode('.jpg', img_contours)
        jpg_as_text = base64.b64encode(buffer)
        result = {
            "type": "error1",
            "image": str(jpg_as_text),
            "example": str(jpg_as_text_examples)
        }
        return result

    width = max_possible.bounding_react_with
    height = max_possible.bounding_react_height
    all_possible = resize_image(width,  height, max_area_possible.roi)
    cv2.imwrite("output/all_possible.png", all_possible)

    # check contours after resize image by image exmaples
    thresh = convert_image_to_thresh(all_possible)
    cv2.imwrite("output/thresh_error2.png", thresh)
    img_contours, detect_possibles, max_area_possible = find_contours(
        rotationed)
    examples = example_possibles.possibles
    is_error2 = False

    sorted_ctrs_examples = sorted(
        examples, key=lambda ctr: cv2.boundingRect(ctr.contour)[1])
    sorted_ctrs_detect_possibles = sorted(
        detect_possibles, key=lambda ctr: cv2.boundingRect(ctr.contour)[1])

    # for i in range(0, len(sorted_ctrs_examples)):
    #     print("x:", str(sorted_ctrs_examples[i].bounding_react_x))
    #     print("y:", str(sorted_ctrs_examples[i].bounding_react_y))
    #     cv2.imwrite("output/sorted_"+str(i)+".png",
    #                 sorted_ctrs_examples[i].roi)
    #     print("=================")
    error_possibles = []
    print("*** Calculator area errror ***")
    print("* Total contours: ", str(len(detect_possibles)))
    print("-----------------------------------")
    for i in range(0, len(sorted_ctrs_detect_possibles)):
        # print("x:", str(sorted_ctrs_detect_possibles[i].bounding_react_x))
        # print("y:", str(sorted_ctrs_detect_possibles[i].bounding_react_y))
        # cv2.imwrite("output/sorted_detect_"+str(i)+".png",
        #             sorted_ctrs_detect_possibles[i].roi)
        area_detect = sorted_ctrs_detect_possibles[i].bounding_react_area
        area_examples = sorted_ctrs_examples[i].bounding_react_area
        sub_area = abs(area_detect-area_examples)
        error = False
        if(sub_area > 1000):
            error_possibles.append(sorted_ctrs_detect_possibles[i])
            error = True
        print("* index: ", str(i))
        print("* are example", str(i) + ": "+str(area_examples))
        print("* are detect", str(i) + ": "+str(area_detect))
        print("* sub area: ", str(sub_area))
        print("* error: ", str(error))
        print("------------------------------------")

    if len(error_possibles) == 0:
        ret, buffer = cv2.imencode('.jpg', img_contours)
        jpg_as_text = base64.b64encode(buffer)
        result = {
            "type": "good",
            "image": str(jpg_as_text),
            "example": str(jpg_as_text_examples)
        }
        return result

    # draw rect error
    for i in range(0, len(error_possibles)):
        w = error_possibles[i].bounding_react_with
        h = error_possibles[i].bounding_react_height
        x_min = error_possibles[i].bounding_react_x
        y_min = error_possibles[i].bounding_react_y
        x_max = x_min + w
        y_max = y_min + h
        # print("x: ", str(x_min))
        # print("x_max", str(x_max))
        cv2.rectangle(img_contours, (x_min, y_min),
                      (x_max, y_max), (0, 0, 255), 2)
    cv2.imwrite("output/result_detect_error.png", img_contours)

    # convert image to base64
    ret, buffer = cv2.imencode('.jpg', img_contours)
    jpg_as_text = base64.b64encode(buffer)
    # print(jpg_as_text)
    result = {
        "type": "error2",
        "image": str(jpg_as_text),
        "example": str(jpg_as_text_examples)
    }
    return result
