import cv2
import numpy as np


def processing_images(img):
    try:
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)
        edge = cv2.Canny(gray, 100, 200)
        _, contours, _ = cv2.findContours(edge.copy(), 1, 1)

        # highlight contours
        cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
        gray = cv2.bitwise_not(gray)
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return thresh
    except Exception as ex:
        print("[Error] :", ex)
        return None


def background_subtraction(backround, img):
    try:
        diff = cv2.absdiff(backround, img)
        _, contours, hierarchy = cv2.findContours(
            diff, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        height, width = diff.shape
        img_contours = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)
        return diff
    except Exception as ex:
        print("[Error] ", ex)
        return None


def rotation_react(thresh):
    try:
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
        return thresh
    except Exception as ex:
        print("[Error] ",  ex)
        return None
