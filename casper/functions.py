import math
import cv2


class Circle:
    def __init__(self, cntr):
        self.contour = cntr
        self.bounding_react = cv2.boundingRect(self.contour)
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


def check_circle(possible):
    try:

        if(possible.bounding_react_area > 100):
            # if(possible.bounding_react_area > 20 and possible.bounding_react_area < 100000 and possible.bounding_react_height > 100 and possible.bounding_react_height < 150):
            return True
        return False
    except Exception as err:
        print(err)
        return False
