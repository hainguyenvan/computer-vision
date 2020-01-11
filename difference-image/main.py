from skimage.measure import compare_ssim
import imutils
import cv2

img_error = "error.JPG"
img_good = "good.JPG"

# load img
error = cv2.imread(img_error)
good = cv2.imread(img_good)

# convert the images to grayscale
gray_error = cv2.cvtColor(error, cv2.COLOR_BGR2GRAY)
gray_good = cv2.cvtColor(good, cv2.COLOR_BGR2GRAY)

# compare
(score,  diff) = compare_ssim(gray_error, gray_good,  full=True)
diff = (diff * 255).astype("uint8")
print("SSIM score: {}".format(score))

thresh = cv2.threshold(
    diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# show image
cv2.imshow("gray error", gray_error)
cv2.imshow("gray good", gray_good)
cv2.imshow("diff", diff)
cv2.imshow("thresh", thresh)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
print("Len cnts: ", str(len(cnts)))
cv2.waitKey(0)
# cnts = imutils.grab_contours(cnts)
