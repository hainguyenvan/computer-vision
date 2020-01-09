import math
import cv2
import numpy as np

output_image = "/home/user1/Project/casper/101/image"


class Circle:
    def __init__(self, cntr):
        self.contour = cntr
        self.bounding_react = cv2.boundingRect(self.contour)
        self.peri = cv2.arcLength(cntr, True)

        [x, y, w, h] = self.bounding_react
        self.bounding_react_x = x
        self.bounding_react_y = y
        self.bounding_react_with = w
        self.bounding_react_height = h

        self.bounding_react_area = w*h
        self.center_x = (x+x+w)/2
        self.center_y = (y+y+h)/2
        self.diagonalSize = math.sqrt((w**2)+(h**2))
        self.aspect_ratio = float(w/h)
        self.approx = cv2.approxPolyDP(cntr, 0.04 * self.peri, True)


def remove_lower_number_px(possible, number_px):
    area = possible.bounding_react_area
    if area < number_px:
        return True
    return False


def detect_object(possible):
    try:
        area = possible.bounding_react_area
        # print('Area: ', str(area))
        if area > 50000 and area < 60000:
            return True
        return False
    except Exception as err:
        print(err)
        return False


def check_circle(possible):
    try:
        area = possible.bounding_react_area
        edeg_shape = len(possible.approx)
        width = possible.bounding_react_with
        height = possible.bounding_react_height
        x = possible.bounding_react_x
        y = possible.bounding_react_y
        ratio = possible.aspect_ratio

        if area > 100 and edeg_shape > 5 and width < 150 and width > 40 and height < 350:
            return True
        # if area > 40 and area < 150 and edeg_shape > 5:
        #     return True
        # if(possible.bounding_react_area > 40):
        #     # if(possible.bounding_react_area > 20 and possible.bounding_react_area < 100000 and possible.bounding_react_height > 100 and possible.bounding_react_height < 150):
        #     return True
        return False
    except Exception as err:
        print(err)
        return False


def detect(thresh, index):
    try:
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        height, width = thresh.shape
        img_contours = np.zeros((height, width, 3), dtype=np.uint8)
        possible_circles = []
        possible_expects = []

        # check object
        is_object = False
        for i in range(0, len(contours)):
              # draw contours based on actual found contours of thresh image
            cv2.drawContours(img_contours, contours, i, (255, 255, 255))

            possible = Circle(contours[i])
            is_object = detect_object(possible)
            if is_object == True:
                break
        if is_object == False:
            return None
        # end check object

        # check error
        for i in range(0, len(contours)):
            # draw contours based on actual found contours of thresh image
            cv2.drawContours(img_contours, contours, i, (255, 255, 255))

            possible = Circle(contours[i])

            # remove lower 15px
            is_lower_px = remove_lower_number_px(possible, 150)
            if is_lower_px == False:
                possible_circles.append(possible)
            # is_circle = check_circle(possible)
            # if is_circle is True:
            #     # print("is_circel: " + str(is_circle))
            #     # print("area: " + str(possible.bounding_react_area))
            #     possible_circles.append(possible)

        # for possible in possible_circles:
        #     is_circle = check_circle(possible)
        #     if is_circle == True:
        #         possible_expects.append(possible)

        image_contours = np.zeros((height, width, 3), np.uint8)
        ctrs = []
        for circle in possible_circles:
            ctrs.append(circle.contour)
        cv2.drawContours(image_contours, ctrs, -1, (255, 255, 255))

        str_name = output_image + "/" + str(index) + ".png"
        cv2.imwrite(str_name, image_contours)
        # print("==== len: ", str(len(possible_circles)))
        if len(possible_circles) <= 13:
            return "error"
        else:
            return "good"
    except Exception as err:
        print(err)
