import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "courses.json"


class CourseRepository:

    def __init__(self):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.courses = data["courses"]

    def get_all(self):
        return self.courses

    def get_by_id(self, course_id):
        for course in self.courses:
            if course["id"] == course_id:
                return course

        return None

    def create(self, course_data):
        new_id = max(
            (course["id"] for course in self.courses),
            default=0
        ) + 1

        new_course = {
            "id": new_id,
            **course_data
        }

        self.courses.append(new_course)

        return new_course

    def delete(self, course_id):
        course = self.get_by_id(course_id)

        if course is None:
            return False

        self.courses.remove(course)

        return True