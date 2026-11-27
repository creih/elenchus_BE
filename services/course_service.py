class CourseService:

    def __init__(self, repository):
        self.repository = repository

    def get_all_courses(self):
        return self.repository.get_all()

    def get_course(self, course_id):
        course = self.repository.get_by_id(course_id)

        if course is None:
            raise ValueError("Course not found")

        return course

    def create_course(self, course_data):
        self.validate_course(course_data)

        return self.repository.create(course_data)

    def delete_course(self, course_id):
        deleted = self.repository.delete(course_id)

        if not deleted:
            raise ValueError("Course not found")

    def validate_course(self, course_data):
        required_fields = [
            "title",
            "description",
            "price",
            "currency"
        ]

        for field in required_fields:
            if field not in course_data:
                raise ValueError(
                    f"Missing required field: {field}"
                )

        if (
            not isinstance(course_data["title"], str)
            or not course_data["title"].strip()
        ):
            raise ValueError(
                "Title must be a non-empty string"
            )

        if (
            not isinstance(course_data["description"], str)
            or not course_data["description"].strip()
        ):
            raise ValueError(
                "Description must be a non-empty string"
            )

        price = course_data["price"]

        if (
            isinstance(price, bool)
            or not isinstance(price, int)
            or price < 0
        ):
            raise ValueError(
                "Price must be a non-negative integer"
            )

        if (
            not isinstance(course_data["currency"], str)
            or not course_data["currency"].strip()
        ):
            raise ValueError(
                "Currency must be a non-empty string"
            )

        return {
            "title": course_data["title"].strip(),
            "description": course_data["description"].strip(),
            "price": price,
            "currency": course_data["currency"].strip()
        }
