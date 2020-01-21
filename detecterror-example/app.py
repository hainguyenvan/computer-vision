import json
import base64
import cv2

from io import BytesIO
from PIL import Image

from flask_cors import CORS
from flask import Flask
from flask import request

from handler_request import (handle_detect, handle_image_examples)

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    result = {
        "status": 200,
        "message": "Successfully"
    }
    return json.dumps(result)


@app.route("/casper/image-background", methods=["POST"])
def handle_request_image_background():
    result = {
        "status": 200,
        "message": "Successfully"
    }
    return json.dumps(result)


@app.route("/casper/image-examples", methods=["POST"])
def handle_request_image_examples():
    print("[Info] sent image examples")
    json_body = json.loads(request.data)
    img_base64 = json_body.get("image")
    im = Image.open(BytesIO(base64.b64decode(img_base64)))
    im.save("output/exmaple_input.png", 'PNG')
    # end body

    img = cv2.imread("output/exmaple_input.png")
    handler_example = handle_image_examples(img)
    # print(str(handler_example))
    result = {
        "status": 200,
        "message": "Successfully",
        "data": {
            "image": str(handler_example)
        }
    }
    return json.dumps(result)


@app.route("/casper/detects", methods=["POST"])
def handle_request_detects():
    print("[Info] sent image detects")
    # data = request.get_json()
    # img_base64 = data.get("body").get("image")
    json_body = json.loads(request.data)
    img_base64 = json_body.get("image")
    im = Image.open(BytesIO(base64.b64decode(img_base64)))
    im.save("output/detect_input.png", 'PNG')
    # end body

    img = cv2.imread("output/detect_input.png")
    handle_detect_result = handle_detect(img)
    result = {
        "status": 200,
        "message": "Successfully",
        "data": handle_detect_result
    }
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
