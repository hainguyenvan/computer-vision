import cv2

from handler_request import handle_image_examples, handle_detect


def test_handle_image_examples():
    img = cv2.imread("input/good.jpg")
    handle_image_examples(img)


def test_handle_detect():
    img = cv2.imread("input/error2.jpg")
    detect = handle_detect(img)
    print("Detect: ", detect)


# test_handle_image_examples()
test_handle_detect()
