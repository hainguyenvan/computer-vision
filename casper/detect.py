# import
import cv2
import numpy as np
import math

import functions

total_error = 0
total_good = 0
img_input = "good.JPG"


def detect_error():
    img = cv2.imread(img_input)

    print("Step 1: Convert images to HSV")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    cv2.imwrite("1.hsv.png", value)

    print("Step 2: Get topHat/blackHat")
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    top_hat = cv2.morphologyEx(value, cv2.MORPH_TOPHAT, kernel)
    black_hat = cv2.morphologyEx(value, cv2.MORPH_BLACKHAT, kernel)
    cv2.imwrite("2.tophat.png", top_hat)
    cv2.imwrite("2.blackhat.png", black_hat)

    print("Step 3: Add and subtract between morphological operations")
    add = cv2.add(value, top_hat)
    subtract = cv2.subtract(add, black_hat)
    cv2.imwrite("3.subtract.png", subtract)

    print("Step 4: Applying gaussian blur on subtract images")
    blur = cv2.GaussianBlur(subtract, (5, 5), 0)
    cv2.imwrite("4.blur.png", blur)

    print("Step 5: Thresholding")
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    cv2.imwrite("5.thresh.png", thresh)

    print("Step 6: Find contours")
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # _, contours, hierarchy = cv2.findContours(
    #     thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # get hight and width of images
    print("-> Get hight/width of images")
    height, width = thresh.shape
    print("hight:" + str(height))
    print("width:"+str(width))
    print("len:" + str(len(contours)))

    img_contours = np.zeros((height, width, 3), dtype=np.uint8)
    possible_circles = []

    # check object
    is_object = False
    for i in range(0, len(contours)):
          # draw contours based on actual found contours of thresh image
        cv2.drawContours(img_contours, contours, i, (255, 255, 255))

        possible = functions.Circle(contours[i])
        is_object = functions.detect_object(possible)
        if is_object:
            break
    # check
    if not is_object:
        return
    # end check object

    # check error
    for i in range(0, len(contours)):
        # draw contours based on actual found contours of thresh image
        cv2.drawContours(img_contours, contours, i, (255, 255, 255))

        possible = functions.Circle(contours[i])
        is_circle = functions.check_circle(possible)
        if is_circle is True:
            print("is_circel: " + str(is_error1))
            print("area: " + str(possible.bounding_react_area))
            possible_circles.append(possible)

    if len(possible_circles) == 0:
        total_error += 1
    else:
        total_good += 1
    cv2.imwrite("6.contours.png", img_contours)

    print("Step 7: Populatiing ctrs list with each circle of possible circles")
    image_contours = np.zeros((height, width, 3), np.uint8)
    ctrs = []
    for circle in possible_circles:
        ctrs.append(circle.contour)
    cv2.drawContours(image_contours, ctrs, -1, (255, 255, 255))
    cv2.imwrite("7.area.png", image_contours)


if __name__ == "__main__":
    print("=== Detects Error Of Casper ===")
    detect_error()
    print("* Statistic:")
    str_total = str(total_good + total_error)
    str_total_good = str(total_good)+"/"+str(total_good + total_error)
    str_total_error1 = str(total_error)+"/"+str(total_good + total_error)
    print("Good: ", str_total_good)
    print("Error: ", str_total_error1)
    print("Total: ", str_total)
    print("=== End Detects Error ====")
