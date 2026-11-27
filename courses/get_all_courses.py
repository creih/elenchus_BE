"""
    this will be the individual file for the api to all of get courses' related ops
    within our memory so far.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "courses.json", "r", encoding="utf-8") as course_file:
    data = json.load(course_file)
courses = data["courses"]

class RequestHandler(BaseHTTPRequestHandler):
    """ class handler for get method. """
    def __init__(self, *args, **kwargs):
        """ initialising the class and its parameters."""
        self.request_started_at = 0.0
        super().__init__(*args, **kwargs)

    def send_json(self, status_code, json_data, content_type, extra_headers=None):
        """the structure of how json typed response should be for code reusability"""
        body = json.dumps(json_data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))

        if extra_headers:
            for header, value in extra_headers.items():
                self.send_header(header, value)

        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """ specifying the first get returning a greetings string. """
        if self.path == "/":
            message = "Hello dear, from elenchus. "
            body = message.encode("utf-8")

            self.send_json(200, json_data=body, content_type="text/plain; charset=utf-8")

        elif self.path == "/courses":
            self.send_json(
                status_code=200,
                json_data= courses,
                content_type="application/json"
            )

        elif self.path.startswith("/courses/"):
            parts = self.path.split("/")

            if len(parts) != 3 or not parts[2]:
                self.send_error(400, "Invalid course ID.")
                return
            try:
                course_id = int(parts[2])
            except ValueError:
                self.send_error(400, "course ID must be an integer.")
                return
            course = None

            for item in courses:
                if item["id"] == course_id:
                    course = item
                    break
            if course is None:
                self.send_error(404, "course not found")
                return
            self.send_json(
                status_code = 200,
                json_data = course,
                content_type = "application/json"
            )
        else:
            message = "Not Found"
            body = message.encode("utf-8")

            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)
