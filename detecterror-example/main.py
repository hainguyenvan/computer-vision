import cgi
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep


PORT_NUMBER = 8080


class RequestHandler(BaseHTTPRequestHandler):
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
            print("Body: ", str(body))
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

        if self.path == "/image-examples":
            print("[Info] sent image examples")
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

        if self.path == "/detects":
            print("[Info] sent image detects")
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
