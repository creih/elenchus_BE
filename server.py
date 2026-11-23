"""
    The servicing file 
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "courses.json", "r", encoding="utf-8") as courses_file:
    data = json.load(courses_file)

courses = data["courses"]

class RequestHandler(BaseHTTPRequestHandler):
    """ this class is for the server response. """
    def do_GET(self):
        """ the get method. """
        if self.path == "/":
            message = "Hello from Elenchus"
            body = message.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        elif self.path== "/courses":
            body = json.dumps({
                "courses": courses
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:
            message = "Not Found"
            body = message.encode("utf-8")

            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)


def main():
    """ main function. """
    parser = argparse.ArgumentParser(
        description="Elenchus HTTP Server"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on"
    )

    args = parser.parse_args()

    server_address = ("", args.port)

    httpd = HTTPServer(server_address, RequestHandler)

    print(f"Elenchus server running on port {args.port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
