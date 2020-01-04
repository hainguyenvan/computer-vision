import cv2
import numpy as np

if __name__ == "__main__":
    # read source image
    img_src = cv2.imread("good1.JPG")
    # four corners of the book in source image
    pts_src = np.array([[141, 131], [480, 159], [493, 630], [64, 601]])

    # read destination image
    img_dst = cv2.imread("good2.JPG")
    # four corners of the book in destination image
    pts_dst = np.array([[318, 256], [534, 372], [316, 670], [73, 473]])

    # calculate homegraphy
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(
        img_src, h, (img_dst.shape[1], img_dst.shape[0]))
    cv2.imwrite("3.homography.png",  im_out)
