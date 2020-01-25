# import packages
import cv2
import numpy as np
import os

from .jaccard_similarity import (JaccardBox, jaccard_similarity)
from .utils import (find_contours)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# input: Thresh images


def detect_error1(jaccard_box_detects, jaccard_box_samples):
    error_possibles = []
    for i in range(0, len(jaccard_box_samples)):
        jaccard_index = -1

        # print("i: ", str(i))
        # print("area: ", str(jaccard_box_samples[i].area))
        # print("x: ", str(jaccard_box_samples[i].x_min))
        # print("y: ", str(jaccard_box_samples[i].y_min))
        # print("width: ", str(jaccard_box_samples[i].width))
        # print("height:", str(jaccard_box_samples[i].height))
        # cv2.imwrite(ROOT_DIR+"/output/"+str(i)+"_jaccard.png",
        #             jaccard_box_samples[i].possible.roi)
        # print("-------------------------")
        for j in range(0, len(jaccard_box_detects)):
            index = jaccard_similarity(
                jaccard_box_samples[i], jaccard_box_detects[j])
            # print("x: ", str(jaccard_box_detects[j].x_min))
            # print("y: ", str(jaccard_box_detects[j].y_min))
            # print("j: ", str(j))
            # print("index: ", str(index))
            # print("area test: ", str(jaccard_box_detects[j].area))
            # print("width: ", str(jaccard_box_detects[j].width))
            # print("height:", str(jaccard_box_detects[j].height))
            cv2.imwrite(ROOT_DIR+"/output/"+str(i)+"_"+str(j)+"_jaccard.png",
                        jaccard_box_detects[j].possible.roi)
            if index > 0 and index < 2:
                jaccard_index = index
                break
        # print("==========")
        # print("jaccard index: ", str(jaccard_index))
        if jaccard_index < 0 or jaccard_index >= 2:
            error_possibles.append(jaccard_box_samples[i])
    return error_possibles
