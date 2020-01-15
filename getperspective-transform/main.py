import numpy as np
import cv2


def order_pointers(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(img, pts):
    rect = order_pointers(pts)
    (tl, tr, br, bl) = rect
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))

    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))

    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (max_width, max_height))
    return warped


img_input = "original image.jpg"
# [(73, 239), (356, 117), (475, 265), (187, 443)]
# top-left:(x,y)
# top-right:(x,y)
# bot-right:(x,y)
# bottom-left:(x,y)
coords = "[(73, 239), (356, 117), (475, 265), (205, 470)]"

img = cv2.imread(img_input)
pts = np.array(eval(coords), dtype="float32")

warped = four_point_transform(img, pts)
cv2.imshow("Original", img)
cv2.imshow("Wraped", warped)
cv2.waitKey(0)
