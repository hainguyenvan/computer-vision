import cv2
import numpy as np


def processing_images(img):
   try:
     if img is None:
       return None

      # pre images
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (11, 11), 0)
      edge = cv2.Canny(gray, 100, 200)
      contours, _ = cv2.findContours(edge.copy(), 1, 1)

      # highlight contours
      cv2.drawContours(gray, contours, -1, [0, 255, 0], 2)
      gray = cv2.bitwise_not(gray)

      thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
      return thresh
    except Exception as ex:
      print("[Error] ", ex)
      return None

def rotation_react(thresh):
  try:
    # coords
    coords = np.column_stack(np.where(thresh == 0))
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    if angle < -45:
          angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = thresh.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return thresh
  except Exception as ex:
    print("[Error] ",  ex)
    return None 
