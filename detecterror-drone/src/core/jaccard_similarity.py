# import packages
from collections import namedtuple
import numpy as np
import cv2


class JaccardBox:
    def __init__(self, x, y, width, height):
        self.x_min = x
        self.y_min = y
        self.x_max = x+width
        self.y_max = y+height
        self.width = width
        self.height = height
        self.area = width * height


# box_a: JaccardBox
# box_b: JaccardBox
def jaccard_similarity(box_a,  box_b):
    # determine the (x,y)-coordinates of the intersection rectangle
    x_min = min(box_a.x_min,  box_b.x_min)
    x_max = max(box_a.x_max, box_b.x_max)

    y_min = min(box_a.y_min, box_b.y_min)
    y_max = max(box_a.y_max, box_b.y_max)

    # compute the area of intersection rectangle
    inter_area = max(0, x_max - x_min)*max(0, y_max - y_min)

    # compute the Jaccard index value by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    jaccard_index = inter_area / float(box_a.area + box_b.area - inter_area)

    # reutrn the jaccard index value value
    return jaccard_index
