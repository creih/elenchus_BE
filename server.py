"""
    The servicing file 
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import json
from pathlib import Path
import logging
import time

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "courses.json", "r", encoding="utf-8") as courses_file:
    data = json.load(courses_file)

courses = data["courses"]

class RequestHandler(BaseHTTPRequestHandler):
    """ this class is for the server response. """
    def __init__(self, *args, **kwargs):
        self.request_started_at = 0.0
        super().__init__(*args, **kwargs)

    def method_not_allowed(self):
        """ customising unidentified methods' responses. """
        path = self.path.split("?")[0]

        allowed_methods = {
            "/": ["GET"],
            "/courses": ["GET", "POST"],
        }

        if path.startswith("/courses/"):
            allowed_methods[path] = ["GET"]

        methods = allowed_methods.get(path)

        if methods is None:
            self.send_json(404, {"error": "Resource not found"})
            return

        self.send_json(
            405,
            {"error": "Method not allowed"},
            {"Allow": ", ".join(methods)}
        )

    def send_json(self, status_code, data, extra_headers=None):
        """ coupling these json process in a function for code reusability"""
        body = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8") # add type to the function parameters too.
        self.send_header("Content-Length", str(len(body)))

        if extra_headers:
            for header, value in extra_headers.items():
                self.send_header(header, value)

        self.end_headers()
        self.wfile.write(body)

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
        elif self.path.startswith("/courses/"):
            parts = self.path.split("/")

            if len(parts) != 3 or not parts[2]:
                self.send_error(400, "Invalid course ID")
                return

            try:
                course_id = int(parts[2])
            except ValueError:
                self.send_error(400, "Course ID must be an integer")
                return

            course = None

            for item in courses:
                if item["id"] == course_id:
                    course = item
                    break

            if course is None:
                self.send_error(404, "Course not found")
                return

            body = json.dumps(course).encode("utf-8")

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

    def do_POST(self):
        """ the post method for nnew course. """
        if self.path != "/courses":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        # 1. Validate Content-Type
        content_type = self.headers.get("Content-Type", "")
        media_type = content_type.split(";")[0].strip().lower()

        if media_type != "application/json":
            self.send_json(415, {"error": "Content-Type must be application/json"})
            return

        # 2. Read Content-Length
        content_length = self.headers.get("Content-Length")

        if content_length is None:
            self.send_json(411, {"error": "Content-Length is required"})
            return

        try:
            content_length = int(content_length)
        except ValueError:
            self.send_json(400, {"error": "Invalid Content-Length"})
            return

        if content_length <= 0:
            self.send_json(400, {"error": "Request body cannot be empty"})
            return

        # 3. Read request body
        body = self.rfile.read(content_length)

        if len(body) != content_length:
            self.send_json(400, {"error": "Incomplete request body"})
            return

        # 4. Parse JSON
        try:
            course_data = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"error": "Invalid JSON"})
            return

        # 5. Validate JSON structure
        if not isinstance(course_data, dict):
            self.send_json(400, {"error": "Request body must be a JSON object"})
            return

        required_fields = ["title", "description", "price", "currency"]

        for field in required_fields:
            if field not in course_data:
                self.send_json(400, {"error": f"Missing required field: {field}"})
                return

        # 6. Validate field values
        if not isinstance(course_data["title"], str) or not course_data["title"].strip():
            self.send_json(400, {"error": "Title must be a non-empty string"})
            return

        if not isinstance(course_data["description"], str) or not course_data["description"].strip():
            self.send_json(400, {"error": "Description must be a non-empty string"})
            return

        if not isinstance(course_data["price"], int) or course_data["price"] < 0:
            self.send_json(400, {"error": "Price must be a non-negative integer"})
            return

        if not isinstance(course_data["currency"], str) or not course_data["currency"].strip():
            self.send_json(400, {"error": "Currency must be a non-empty string"})
            return

        # 7. Generate a new ID
        new_id = max(
            (course["id"] for course in courses),
            default=0
        ) + 1

        new_course = {
            "id": new_id,
            "title": course_data["title"].strip(),
            "description": course_data["description"].strip(),
            "price": course_data["price"],
            "currency": course_data["currency"].strip()
        }

        # 8. Store course in memory
        courses.append(new_course)

        # 9. Return 201 Created
        self.send_json(
            201,
            new_course,
            {"Location": f"/courses/{new_id}"}
        )
    def do_DELETE(self):
        """ delete not yet implemented"""
        self.method_not_allowed()

    def do_PUT(self):
        """ put for updating not yet implemented"""
        self.method_not_allowed()

    def do_PATCH(self):
        """ patch same as put not yet implemented"""
        self.method_not_allowed()

    def handle_one_request(self):
        self.request_started_at = time.perf_counter()
        super().handle_one_request()


    def log_request(self, code="-", size="-"):
        duration = (
            time.perf_counter() - self.request_started_at
        ) * 1000

        logging.info(
            "%s %s %s %.2fms",
            self.command,
            self.path,
            code,
            duration
        )

def main():
    """ main function. """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

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
