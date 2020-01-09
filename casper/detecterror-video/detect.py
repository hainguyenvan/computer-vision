import cv2

import functions

print("=== Casper Object Detect Error ===")
output_image = "/home/user1/Project/casper/101/image"
cap = cv2.VideoCapture("video.mp4")

index = 0
current_type = "nan"
while True:
    ret, frame = cap.read()
    # frame2 = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    blur = cv2.GaussianBlur(value, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2)
    # _, contours, hierarchy = cv2.findContours(
    #     thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # file_name = str(index) + ".png"
    # cv2.imwrite(output_image + "/"+file_name, thresh)
    cv2.imshow("frame",  frame)
    cv2.imshow("thresh", thresh)
    detect = functions.detect(thresh,  index)
    if detect is not None:
        if detect != current_type:
            current_type = detect
            print("* Type: ", current_type)
    index += 1
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
