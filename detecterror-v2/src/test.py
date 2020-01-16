import cv2

from translations import background_subtraction
from handle_request import handle_example_image, handle_background, handle_detect


def test_background_subtracttions():
    background_input_img = "output/resize.png"
    input_img = "output/227.png"

    background_img = cv2.imread(background_input_img)
    # background_img = processing_images(background_img)

    img = cv2.imread(input_img)
    # img = processing_images(img)

    diff = background_subtraction(background_img, img)
    cv2.imwrite("output/diff.png", diff)


def resize_image():
    pattern_img = cv2.imread("output/227.png")
    resize_img = cv2.imread("output/6.png")
    height, width, channels = pattern_img.shape
    dim = (width, height)
    resized = cv2.resize(resize_img, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite("output/resize.png", resized)


def test_handle_example_image():
    img = cv2.imread("input/good.jpg")
    example_img = handle_example_image(img)
    cv2.imwrite("pattern/example.png", example_img)


def test_handle_background():
    img = cv2.imread("input/background.jpg")
    background = handle_background(img)
    cv2.imwrite("pattern/background.png", background)


def test_handle_detect():
    # img = cv2.imread("input/error2_3.jpg")
    # img = cv2.imread("input/error1_1.jpg")
    img = cv2.imread("input/error2.jpg")
    detect = handle_detect(img)
    print("Result detect: ", detect)


# resize_image()
# test_background_subtracttions()
# test_handle_example_image()
# test_handle_background()
test_handle_detect()
