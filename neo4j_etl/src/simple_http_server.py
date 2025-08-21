import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        base_dir = os.path.join(os.getcwd(), 'data')
        path = os.path.normpath(SimpleHTTPRequestHandler.translate_path(self, path))
        return os.path.join(base_dir, os.path.relpath(path, os.getcwd()))

def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run(HTTPServer, CustomHTTPRequestHandler, PORT)
