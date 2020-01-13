import cv2
from imutils.video import FPS
import imutils
import numpy as np

import detects

# define input
path_video = "/home/user1/Project/casper/face/video2.mp4"
output_img = "/home/user1/Project/casper/face/image2"
model_path = "v3.0_200k.tflite"
score = 0.4
detect_loop = 5
# end define input


cap = cv2.VideoCapture(path_video)
fps = FPS().start()

index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    height, width, layers = frame.shape
    new_h = int(height/2)
    new_w = int(width/2)
    frame_resize = cv2.resize(frame, (new_w, new_h))
    # frame = imutils.resize(frame, width=640)
    img_output = output_img+"/"+str(index)+".png"
    cv2.imwrite(img_output, frame)
    people_count = detects.detect(img_output, model_path, score, detect_loop)
    cv2.imshow("Video", frame)
    index += 1

    key = cv2.waitKey(25)
    if key == 113:
        break

fps.stop()
cap.release()
cv2.destroyAllWindows()
