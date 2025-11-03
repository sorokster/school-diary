from django.test import TestCase, Client


# Create your tests here.
class TestTeacherEndpointsWithNotTeacherRights(TestCase):
    fixtures = ["fixtures/data.json"]

    def setUp(self):
        self.client = Client()
        self.client.login(username="student1", password="1234")

    def test_lessons_view_with_student_user(self):
        response = self.client.get("/teacher/lessons/")
        self.assertEqual(response.status_code, 403)

    def test_lessons_view_redirects_anonymous_user(self):
        self.client.logout()

        response = self.client.get("/teacher/lessons/")
        self.assertEqual(response.status_code, 302)


class TestTeacherEndpointsWithTeacherRights(TestCase):
    fixtures = ["fixtures/data.json"]
    def setUp(self):
        self.client = Client()
        self.client.login(username="sorokster", password="1234")

    def test_lessons_view_with_teacher_user(self):
        response = self.client.get("/teacher/lessons/")
        self.assertEqual(response.status_code, 200)

    def test_lesson_existing_view(self):
        response = self.client.get("/teacher/lessons/1/")
        self.assertEqual(response.status_code, 200)

    def test_lesson_not_existing_view(self):
        response = self.client.get("/teacher/lessons/10/")
        self.assertEqual(response.status_code, 404)

    def test_lesson_creation(self):
        response = self.client.post("/teacher/lessons/", {
            "name": "Rates and percentages",
            "description": "In these tutorials, we'll look at how rates and percentages relate to proportional thinking. We'll also solve interesting word problems involving percentages (discounts, taxes, and tip calculations).",
            "subject": 1,
            "class": 1,
            "room": 2,
            "date": "2025-11-12"
        })
        self.assertEqual(response.status_code, 302)

    def test_grade_putting(self):
        response = self.client.post("/teacher/homeworks/1/grade/", {
            "grade": 11,
            "feedback": "Nice!",
            "submission": 3,
            "student": 4,
            "graded_at": "2025-11-03"
        })

        self.assertEqual(response.status_code, 302)
