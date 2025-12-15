from http.server import BaseHTTPRequestHandler, HTTPServer
import os


PORT = int(os.getenv("PORT", 8080))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write("ok".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("not found".encode())


if __name__ == "__main__":
    server = HTTPServer(("", PORT), Handler)
    print(f"Server running on port {PORT}")
    server.serve_forever()
