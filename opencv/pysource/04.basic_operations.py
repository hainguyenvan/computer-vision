import cv2
import numpy as np

input_video = "image/good.jpg"
img = cv2.imread(input_video)
rows, col, ch = img.shape
roi = img[100:280,  150:320]
print(img[175, 300])
# change value of a pixe
img[250, 180] = (255, 0, 0)
# save image
cv2.imwrite("image/04.basic_operations.png",  roi)
cv2.destroyAllWindows()
