# import packages
import json
import base64
import cv2

from io import BytesIO
from PIL import Image

from flask_cors import CORS
from flask import Flask
from flask import request

# import handle functions
from core.samples import (save_samples, get_samples)

# create app
app = Flask(__name__)
CORS(app)


# api hello world
@app.route("/")
def index():
    result = {
        "status": 200,
        "message": "Successfully"
    }
    return json.dumps(result)


# api sent background
@app.route("/casper/image-background", methods=["POST"])
def handle_request_image_background():
    # todo-hainv
    result = {
        "status": 200,
        "message": "Successfully"
    }
    return result


# api get image example
@app.route("/casper/image-examples", methods=["GET"])
def handle_request_get_image_examples():
    print("[INFO] Get image examples")
    # get examples
    example_possibles = get_samples()
    ret_examples, buffer_examples = cv2.imencode(
        '.jpg',  example_possibles.max_area_possible.roi)
    jpg_as_text_examples = base64.b64encode(buffer_examples)
    result = {
        "status": 200,
        "message": "Successfully",
        "data": {
            "image":  str(jpg_as_text_examples)
        }
    }
    return json.dumps(result)


# api handle request example
#  body { "image":"base64"}
@app.route("/casper/image-examples", methods=["POST"])
def handle_request_image_examples():
    try:
        print("[INFO] Handle sent image examples")
        # parse body
        json_body = json.loads(request.data)
        img_base64 = json_body.get("image")
        im = Image.open(BytesIO(base64.b64decode(img_base64)))
        im.save("core/images/exmaple_input.png", "PNG")

        # handle example
        img = cv2.imread("core/images/exmaple_input.png")
        example_possibles = save_samples(img)
        cv2.imwrite("core/images/exmaple_handled.png",
                    example_possibles.max_area_possible.roi)
        ret, buffer = cv2.imencode(
            '.jpg', example_possibles.max_area_possible.roi)
        jpg_as_text = base64.b64encode(buffer)

        result = {
            "status": 200,
            "message": "Successfully",
            "data": {
                "image": str(jpg_as_text)
            }
        }
        return json.dumps(result)
    except Exception as ex:
        print("[ERROR] Handle request sent image examples: ", str(ex))
        result = {
            "status":  500,
            "message": str(ex)
        }
        return json.dumps(result)


# run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
