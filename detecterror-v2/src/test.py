import cv2

from translations import processing_images, background_subtraction


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


# resize_image()
test_background_subtracttions()
