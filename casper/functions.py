import math
import cv2


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


def detect_object(possible):
    try:
        area = possible.bounding_react_area
        if area > 150000 and area < 400000:
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
        # x = possible.bounding_react_x
        # y = possible.bounding_react_y

        # if area > 100 and edeg_shape > 5 and width < 150 and height < 350:
        #     return True
        if area > 100 and edeg_shape > 5 and width > 100 and width < 150 and height < 350:
            return True
        # if(possible.bounding_react_area > 40):
        #     # if(possible.bounding_react_area > 20 and possible.bounding_react_area < 100000 and possible.bounding_react_height > 100 and possible.bounding_react_height < 150):
        #     return True
        return False
    except Exception as err:
        print(err)
        return False
