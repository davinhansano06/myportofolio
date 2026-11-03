from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from main.models import Education


class EducationDRFAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users: Owner (superuser), Editor (in group Editor), Regular user
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

        self.regular_user = User.objects.create_user(
            username="regular",
            password="password123",
        )

        # Initial Education data
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            period="2025 - 2029",
            location="Depok, West Java, Indonesia",
            skills="Python, Django, Data Analysis",
            is_current=True,
            logo="img/uiputih.png",
        )

        self.list_url = reverse("api:education_list_create")
        self.detail_url = reverse(
            "api:education_detail",
            kwargs={"pk": self.education.pk},
        )
        self.star_url = reverse(
            "api:education_star",
            kwargs={"pk": self.education.pk},
        )

    def test_public_can_list_and_search_educations(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["institution"],
            "Universitas Indonesia",
        )
        self.assertTrue(response.data[0]["is_current"])

        # Search query matching
        search_hit = self.client.get(f"{self.list_url}?q=Sistem")
        self.assertEqual(search_hit.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_hit.data), 1)

        # Search query non-matching
        search_miss = self.client.get(f"{self.list_url}?q=Harvard")
        self.assertEqual(search_miss.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_miss.data), 0)

    def test_owner_full_crud_and_is_current_checkbox(self):
        self.client.force_authenticate(user=self.owner)

        # Create with is_current=True and HTML tags (sanitized by serializer)
        create_res = self.client.post(
            self.list_url,
            {
                "institution": "<b>SMA Negeri 3 Malang</b>",
                "degree": "IPA",
                "period": "2022 - 2025",
                "location": "Malang",
                "skills": "Mathematics",
                "logo": "img/logosma.jpg",
                "is_current": True,
            },
            format="json",
        )
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_res.data["institution"], "SMA Negeri 3 Malang")
        self.assertTrue(create_res.data["is_current"])
        new_id = create_res.data["id"]

        # Verify is_current persisted in DB
        created_obj = Education.objects.get(pk=new_id)
        self.assertTrue(created_obj.is_current)

        # Update via PATCH (toggle is_current to False)
        new_detail_url = reverse("api:education_detail", kwargs={"pk": new_id})
        patch_res = self.client.patch(
            new_detail_url,
            {"is_current": False, "location": "Malang, Jawa Timur"},
            format="json",
        )
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertFalse(patch_res.data["is_current"])
        self.assertEqual(patch_res.data["location"], "Malang, Jawa Timur")
        created_obj.refresh_from_db()
        self.assertFalse(created_obj.is_current)

        # Update via PUT
        put_res = self.client.put(
            new_detail_url,
            {
                "institution": "SMA Negeri 3 Malang",
                "degree": "MIPA",
                "period": "2022 - 2025",
                "location": "Malang, Indonesia",
                "skills": "Math, Leadership",
                "logo": "img/logosma.jpg",
                "is_current": True,
            },
            format="json",
        )
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data["degree"], "MIPA")
        self.assertTrue(put_res.data["is_current"])

        # Delete via DELETE
        del_res = self.client.delete(new_detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=new_id).exists())

    def test_editor_permissions(self):
        self.client.force_authenticate(user=self.editor)

        # Editor CANNOT create (POST -> 403)
        post_res = self.client.post(
            self.list_url,
            {
                "institution": "Test Edu",
                "degree": "S1",
                "period": "2025",
                "location": "Jakarta",
                "skills": "Testing",
                "logo": "img/logoui.png",
            },
            format="json",
        )
        self.assertEqual(post_res.status_code, status.HTTP_403_FORBIDDEN)

        # Editor CAN update (PATCH -> 200)
        patch_res = self.client.patch(
            self.detail_url,
            {"degree": "S1 Sistem Informasi (Updated by Editor)"},
            format="json",
        )
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            patch_res.data["degree"],
            "S1 Sistem Informasi (Updated by Editor)",
        )

        # Editor CANNOT delete (DELETE -> 403)
        del_res = self.client.delete(self.detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_and_anonymous_permissions(self):
        # Anonymous user cannot POST, PATCH, DELETE, or Star
        self.assertIn(
            self.client.post(self.list_url, {}, format="json").status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertIn(
            self.client.patch(self.detail_url, {}, format="json").status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertIn(
            self.client.delete(self.detail_url).status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertIn(
            self.client.post(self.star_url).status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

        # Regular logged-in user cannot POST, PATCH, or DELETE
        self.client.force_authenticate(user=self.regular_user)
        self.assertEqual(
            self.client.post(self.list_url, {}, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.patch(self.detail_url, {}, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.delete(self.detail_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        # Regular logged-in user CAN Star and Unstar
        star_res = self.client.post(self.star_url)
        self.assertEqual(star_res.status_code, status.HTTP_200_OK)
        self.assertTrue(star_res.data["is_starred"])
        self.assertEqual(star_res.data["star_count"], 1)

        unstar_res = self.client.post(self.star_url)
        self.assertEqual(unstar_res.status_code, status.HTTP_200_OK)
        self.assertFalse(unstar_res.data["is_starred"])
        self.assertEqual(unstar_res.data["star_count"], 0)

