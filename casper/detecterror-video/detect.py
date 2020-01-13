import cv2

import functions

print("=== Casper Object Detect Error ===")
output_image = "/home/user1/Project/casper/101/image"
cap = cv2.VideoCapture("/home/user1/Desktop/Videotest.mp4")

index = 0
current_type = "nan"
total_error = 0
total_good = 0
prev_object = False
index_img = 0
while True:
    ret, frame = cap.read()
    # frame2 = cv2.flip(frame, 1)

    if frame is None:
        break

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
    if detect is None:
        prev_object = False
    elif prev_object == False:
        index_img += 1
        prev_object = True
        # if detect != current_type:
        current_type = detect
        if current_type == "good":
            total_good += 1
        else:
            total_error += 1
        type_msg = str(index_img) + ")Type: " + str(current_type)
        print(type_msg)
    index += 1
    key = cv2.waitKey(1)
    if key == 27:
        break

total = total_error + total_good
print("\n")
print("* Result:")
print("Error: ",  str(total_error)+"/" + str(total))
print("Good: ",  str(total_good)+"/" + str(total))
print("=== Done ===")
cap.release()
cv2.destroyAllWindows()
