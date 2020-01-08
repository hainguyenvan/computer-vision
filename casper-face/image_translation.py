import glob
import os
import cv2
import numpy as np

input_file = "images"
print("=== Image Translation ===")
for pathAndFilename in glob.iglob(os.path.join(input_file, "*")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    filename = title+ext
    input = input_file+'/'+filename
    img = cv2.imread(input)

    print("Image: ", filename)
    # convert hsv
    print("Step 1: Convert images to HSV")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    cv2.imwrite("step1/"+filename, value)

    print("Step 2: Get topHat/blackHat")
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    top_hat = cv2.morphologyEx(value, cv2.MORPH_TOPHAT, kernel)
    black_hat = cv2.morphologyEx(value, cv2.MORPH_BLACKHAT, kernel)
    cv2.imwrite("step2/tophat_"+filename, top_hat)
    cv2.imwrite("step2/blackhat_"+filename, black_hat)

    print("Step 3: Add and subtract between morphological operations")
    add = cv2.add(value, top_hat)
    subtract = cv2.subtract(add, black_hat)
    cv2.imwrite("step3/"+filename, subtract)

    print("Step 4: Applying gaussian blur on subtract images")
    blur = cv2.GaussianBlur(subtract, (5, 5), 0)
    cv2.imwrite("step4/"+filename, blur)

    print("Step 5: Thresholding")
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)
    cv2.imwrite("step5/"+filename, thresh)
    print("\n")
