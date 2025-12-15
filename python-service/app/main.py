from http.server import BaseHTTPRequestHandler, HTTPServer
import os

PORT = int(os.getenv("PORT", "8080"))
MESSAGE = os.getenv("MESSAGE", "Default message")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        elif self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(MESSAGE.encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print("API_KEY loaded:", "API_KEY" in os.environ)
    server = HTTPServer(("", PORT), Handler)
    server.serve_forever()
