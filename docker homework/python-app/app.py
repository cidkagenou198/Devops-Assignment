from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloWorld(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Hello World from Python!</h1>")

server = HTTPServer(("0.0.0.0", 8000), HelloWorld)
print("Server running on port 8000")
server.serve_forever()