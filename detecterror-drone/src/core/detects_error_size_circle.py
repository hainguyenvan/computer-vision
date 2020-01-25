# import package
import cv2
import numpy as np
import os

from .jaccard_similarity import (JaccardBox, jaccard_similarity)
from .utils import (find_contours)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def detect_error_size_circle(jaccard_box_detects, jaccard_box_samples):
    error_possibles = []
    for i in range(0, len(jaccard_box_samples)):
        jaccard_index = -1
        for j in range(0, len(jaccard_box_detects)):
            index = jaccard_similarity(
                jaccard_box_samples[i], jaccard_box_detects[j])
            if index > 0 and index < 1.5:
                jaccard_index = index
                break
        if jaccard_index < 0 or jaccard_index >= 1.5:
            error_possibles.append(jaccard_box_samples[i])
    return error_possibles
