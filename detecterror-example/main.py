import cgi
import json
import base64
import cv2

from io import BytesIO
from PIL import Image

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

from handler_request import (handle_detect, handle_image_examples)


PORT_NUMBER = 8080


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            mimetype = "application/json"
            self.send_header('Content-type', mimetype)
            self.end_headers()
            result = {
                "status": 200,
                "message": "Successfully"
            }
            self.wfile.write(bytes(json.dumps(result), "utf-8"))
            return

    def do_POST(self):
        if self.path == "/background":
            print("[Info] sent background")
            content_len = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_len)
            body = body.decode("utf8")
            body = json.loads(body)
            print("Body: ", body["type"])
            self.send_response(200)
            mimetype = "application/json"
            self.send_header('Content-type', mimetype)
            self.end_headers()
            result = {
                "status": 200,
                "message": "Successfully"
            }
            self.wfile.write(bytes(json.dumps(result), "utf-8"))
            return

        # body {"image":"...."}
        if self.path == "/image-examples":
            print("[Info] sent image examples")
            self.send_response(200)
            mimetype = "application/json"
            self.send_header('Content-type', mimetype)
            self.end_headers()

            # get body
            content_len = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_len)
            body = body.decode("utf8")
            body = json.loads(body)
            # print("Body: ", body["image"])
            img_base64 = body["image"]
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
            self.wfile.write(bytes(json.dumps(result), "utf-8"))
            return

        if self.path == "/detects":
            print("[Info] sent image detects")
            self.send_response(200)
            mimetype = "application/json"
            self.send_header('Content-type', mimetype)
            self.end_headers()

            # get body
            content_len = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_len)
            body = body.decode("utf8")
            body = json.loads(body)
            # print("Body: ", body["image"])
            img_base64 = body["image"]
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
            self.wfile.write(bytes(json.dumps(result), "utf-8"))
            return

        # self._set_response()
        # self.wfile.write("POST request for ".encode('utf-8'))


def main():
    try:
        server = HTTPServer(("", PORT_NUMBER), RequestHandler)
        print("Started http server on port :", str(PORT_NUMBER))
        # Wait forever incoming http requests
        server.serve_forever()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
