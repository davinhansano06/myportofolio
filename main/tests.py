from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from main.models import Education, Experience


class PortfolioRegressionTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="password123",
            email="owner@example.com",
        )
        self.editor = User.objects.create_user(
            username="editor",
            password="password123",
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="Undergraduate Student",
            period="2025 - 2029",
            location="Depok, West Java, Indonesia",
            skills="Computer Science & Data Analysis",
            is_current=True,
            logo="img/uiputih.png",
        )
        self.experience = Experience.objects.create(
            title="Best Team Business Case",
            institution="Ristek Fasilkom UI",
            period="2025",
            description="Won Best Team in Business Case Project.",
            image="img/ristek.jpeg",
        )

    def test_main_page_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_education_page_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, "/api/v1/educations/")

    def test_experience_page_and_json_accessible(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

        json_res = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(json_res.status_code, 200)
        self.assertEqual(len(json_res.json()), 1)

    def test_update_education_page_for_owner_and_editor(self):
        update_url = reverse(
            "main:update_education",
            kwargs={"id": self.education.id},
        )

        # Editor can access update page
        self.client.login(username="editor", password="password123")
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_education.html")
        self.assertContains(
            response,
            f"/api/v1/educations/{self.education.id}/",
        )
