import cv2

video_input = ""
cap = cv2.VideoCapture(video_input)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # show frame
    cv2.imshow("frame", frame)

    # wait break
    key = cv2.waitKey(1)
    if key == 27:
        break

# destroy
cap.release()
cv2.destroyAllWindows()
