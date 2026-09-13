from django.test import TestCase
from django.urls import reverse

from main.models import Education


class EducationPageTest(TestCase):

    def test_education_page_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears(self):
        Education.objects.create(
            institution="Universitas Indonesia",
            degree="Undergraduate Student",
            period="2025 - 2029",
            location="Depok, West Java, Indonesia",
            skills="Computer Science & Data Analysis",
            logo="img/uiputih.png",
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Universitas Indonesia")
        self.assertContains(response, "Undergraduate Student")

    def test_education_empty_state(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "Belum ada pendidikan yang ditambahkan."
        )