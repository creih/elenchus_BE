# import time
# import logging

from http.server import BaseHTTPRequestHandler

from services.course_service import CourseService
from repo.course_repo import CourseRepository
from utils.response import send_json
from utils.validator import parse_json, validate_json_object


repository = CourseRepository()
course_service = CourseService(repository)


class RequestHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, json_data, extra_headers=None):
        send_json(
            self,
            status_code,
            json_data,
            extra_headers
        )
    def do_GET(self):

        if self.path == "/":
            body = b"Hello from Elenchus"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/courses":
            courses = course_service.get_all_courses()

            self.send_json(200, {"courses": courses})

        elif self.path.startswith("/courses/"):
            parts = self.path.split("/")

            if len(parts) != 3 or not parts[2]:
                self.send_json(400, {"error": "Invalid course ID"})
                return

            try:
                course_id = int(parts[2])
                course = course_service.get_course(course_id)

                self.send_json(200, course)

            except ValueError as error:
                if str(error) == "Course not found":
                    self.send_json(404, {"error": str(error)})
                else:
                    self.send_json(400, {"error": "Course ID must be an integer"})

        else:
            self.send_json(404, {"error": "Resource not found"})
    def do_POST(self):

        if self.path != "/courses":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        content_type = self.headers.get("Content-Type", "")
        media_type = content_type.split(";")[0].strip().lower()

        if media_type != "application/json":
            self.send_json(415, {
                "error": "Content-Type must be application/json"
            })
            return

        content_length = self.headers.get("Content-Length")

        if content_length is None:
            self.send_json(411, {
                "error": "Content-Length is required"
            })
            return

        try:
            content_length = int(content_length)

            if content_length <= 0:
                raise ValueError("Request body cannot be empty")

            body = self.rfile.read(content_length)

            if len(body) != content_length:
                raise ValueError("Incomplete request body")

            course_data = validate_json_object(parse_json(body))

            new_course = course_service.create_course(course_data)

            self.send_json(
                201,
                new_course,
                {"Location": f"/courses/{new_course['id']}"}
            )

        except ValueError as error:
            self.send_json(400, {"error": str(error)})
    
    def do_DELETE(self):
        parts = self.path.split("/")

        if len(parts) != 3 or parts[1] != "courses" or not parts[2]:
            self.send_json(404, {"error": "Resource not found"})
            return

        try:
            course_id = int(parts[2])
        except ValueError:
            self.send_json(400, {"error": "Course ID must be an integer"})
            return

        try:
            course_service.delete_course(course_id)

            self.send_response(204)
            self.end_headers()

        except ValueError:
            self.send_json(404, {"error": "Course not found"})
