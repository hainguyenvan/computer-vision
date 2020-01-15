import math
import cv2


class Possible:
    def __init__(self, cntr):
        self.contour = cntr
        self.bounding_react = cv2.boundingRect(self.contour)

        # length edge
        self.peri = cv2.arcLength(cntr, True)
        [x, y, w, h] = self.bounding_react
        self.bounding_react_x = x
        self.bounding_react_y = y
        self.bounding_react_with = w
        self.bounding_react_height = h

        self.bounding_react_area = w*h
        self.center_x = (x+x+w)/2
        self.center_y = (y+y+h)/2
        self.diagonal_size = math.sqrt((w**2)+(h**2))
        self.aspect_ratio = float(w/h)
        # reactangle to shape basic
        self.approx = cv2.approxPolyDP(cntr, 0.04 * self.peri, True)
