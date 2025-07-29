import http.server
import socketserver
import json
import os
import urllib.request

PORT = 5000
JUDGE0_URL = os.environ.get('JUDGE0_URL', 'http://judge0:2358')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            code = data.get('code', '')
            language_id = data.get('language_id', 71)  # 71 = Python 3

            submission = {
                "source_code": code,
                "language_id": language_id,
                "stdin": "3 5\n"
            }
            req = urllib.request.Request(
                f"{JUDGE0_URL}/submissions?base64_encoded=false&wait=true",
                data=json.dumps(submission).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    result = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(result)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Not found")

    def do_GET(self):
        # Serve static files from /app/static
        static_dir = os.path.join(os.getcwd(), "static")
        if self.path == '/':
            self.path = '/index.html'
        file_path = os.path.join(static_dir, self.path.lstrip('/'))
        if os.path.isfile(file_path):
            self.send_response(200)
            if self.path.endswith('.html'):
                self.send_header('Content-Type', 'text/html')
            elif self.path.endswith('.css'):
                self.send_header('Content-Type', 'text/css')
            elif self.path.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript')
            else:
                self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

if __name__ == '__main__':
    # Set working directory to /app (where server.py is)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
