import cv2

# input_url = "rtsp://D32853466:A12345678@192.168.100.5/h264_stream"
input_url = "rtsp://admin:RSEMXM@192.168.100.5:554/H.264"

cap = cv2.VideoCapture(input_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
