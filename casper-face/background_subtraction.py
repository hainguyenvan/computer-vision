import glob
import os
import numpy as np
import cv2

input_file = "images"
output_file = "background-substraction"
substraction = "test200.png"

print("=== Background Subtractions ===")
img_substraction = cv2.imread(substraction)
gray_substraction = cv2.cvtColor(img_substraction, cv2.COLOR_BGR2GRAY)
gray_substraction = cv2.GaussianBlur(gray_substraction, (21, 21), 0)

backSub = cv2.createBackgroundSubtractorMOG2()

print("=== Image Translation ===")
for pathAndFilename in glob.iglob(os.path.join(input_file, "*")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    filename = title+ext
    input = input_file+'/'+filename
    img = cv2.imread(input)

    print("Image: ", filename)
    fgmask = backSub.apply(img)
    cv2.imwrite("step5/"+filename, fgmask)

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # difference = cv2.absdiff(gray, gray_substraction)

    # # Bước 2: Làm mờ ảnh
    # blur = cv2.GaussianBlur(difference, (9, 9), 1)

    # # Bước 3: Lọc nhiễu
    # new = cv2.adaptiveThreshold(
    #     blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, -5)

    # thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    # thresh = cv2.dilate(thresh, None, iterations=2)
    # cv2.imwrite("step5/"+filename, thresh)

    # print("Image: ", filename)
    # difference = cv2.absdiff( img_substraction, img)

    # print("Step 2: Get topHat/blackHat")
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # top_hat = cv2.morphologyEx(difference, cv2.MORPH_TOPHAT, kernel)
    # black_hat = cv2.morphologyEx(difference, cv2.MORPH_BLACKHAT, kernel)
    # cv2.imwrite("step2/tophat_"+filename, top_hat)
    # cv2.imwrite("step2/blackhat_"+filename, black_hat)

    # print("Step 3: Add and subtract between morphological operations")
    # add = cv2.add(difference, top_hat)
    # subtract = cv2.subtract(add, black_hat)
    # cv2.imwrite("step3/"+filename, subtract)

    # print("Step 4: Applying gaussian blur on subtract images")
    # blur = cv2.GaussianBlur(subtract, (5, 5), 0)
    # cv2.imwrite("step4/"+filename, blur)

    # # print("Step 5: Thresholding")
    # thresh = cv2.adaptiveThreshold(
    #     blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    # cv2.imwrite("step5/"+filename, thresh)
    print("\n")
