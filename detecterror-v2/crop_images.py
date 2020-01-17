import cv2
import numpy as np

input_path = "/home/user1/Project/casper/images-processing/detecterror-v2/src/input/"
output_path = "/home/user1/Project/casper/images-processing/detecterror-v2/src/output/"


def rotation_rect(thresh):
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

    gray = cv2.GaussianBlur(rotated, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh


def crop_min_area_rect(thresh):
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print("Len contours: ", str(len(contours)))
    max_cntr = None
    max_area_rect = -1
    for cntr in contours:
        rect = cv2.minAreaRect(cntr)
        w = rect[1][0]
        h = rect[1][1]
        area = w*h
        if max_area_rect < area:
            max_cntr = cntr
            max_area_rect = area

    # coords = np.column_stack(np.where(thresh > 0))
    # rect = cv2.minAreaRect(coords)
    rect = cv2.minAreaRect(max_cntr)
    box = cv2.boxPoints(rect)
    ext_left = tuple(max_cntr[max_cntr[:, :, 0].argmin()][0])
    ext_right = tuple(max_cntr[max_cntr[:, :, 0].argmax()][0])
    ext_top = tuple(max_cntr[max_cntr[:, :, 1].argmin()][0])
    ext_bot = tuple(max_cntr[max_cntr[:, :, 1].argmax()][0])

    roi_corners = np.array([box], dtype=np.int32)
    cv2.polylines(thresh, roi_corners, 1, (255, 0, 0), 1)
    cropped_image = thresh[ext_top[1]:ext_bot[1], ext_left[0]:ext_right[0]]
    cv2.imwrite(output_path+"crop_img.png",  cropped_image)
    return None


def main():
    print("=== Crop Images ===")
    img = cv2.imread(input_path+"error2_3.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    edge = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edge.copy(), 1, 1)
    cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # thresh
    cv2.imwrite(output_path+"thresh.png", thresh)
    # rotation thresh
    thresh = rotation_rect(thresh)
    cv2.imwrite(output_path+"rotation_rect.png", thresh)
    crop_img = crop_min_area_rect(thresh)
    # cv2.imwrite(output_path+"crop_ing.png", crop_img)
    print("=== Done ===")


if __name__ == "__main__":
    main()
