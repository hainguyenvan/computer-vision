import cv2

cap = cv2.VideoCapture(0)

while True:
    # ret: boolean, true is reading a frame
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("frame webcam", frame)

    # wait key and break
    key = cv2.waitKey(1)
    if key == 27:
        break

# destroy
cap.release()
cv2.destroyAllWindows()
