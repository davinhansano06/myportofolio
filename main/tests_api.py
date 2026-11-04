from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, APIClient
from main.models import Education, Experience
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


class ExperienceDRFAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_exp",
            password="password123",
            email="owner_exp@example.com",
        )

        self.editor = User.objects.create_user(
            username="editor_exp",
            password="password123",
        )

        editor_group, _ = Group.objects.get_or_create(
            name="Editor"
        )
        self.editor.groups.add(editor_group)

        self.regular_user = User.objects.create_user(
            username="regular_exp",
            password="password123",
        )

        self.experience = Experience.objects.create(
            title="Staff Sponsorship",
            institution="COMPFEST",
            period="2025",
            description="Managed sponsorship outreach.",
            image="img/compfest.png",
        )

        self.list_url = reverse("api:experience_list_create")
        self.detail_url = reverse(
            "api:experience_detail",
            kwargs={"pk": self.experience.pk},
        )
        self.star_url = reverse(
            "api:experience_star",
            kwargs={"pk": self.experience.pk},
        )

    def test_public_can_list_search_and_view_detail(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Staff Sponsorship",
        )

        search_hit = self.client.get(
            f"{self.list_url}?q=COMPFEST"
        )
        self.assertEqual(search_hit.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_hit.data), 1)

        search_miss = self.client.get(
            f"{self.list_url}?q=Harvard"
        )
        self.assertEqual(search_miss.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_miss.data), 0)

        detail_response = self.client.get(self.detail_url)
        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        initial_count = Experience.objects.count()

        create_response = self.client.post(
            self.list_url,
            {
                "title": "<b>Project Manager</b>",
                "institution": "University Organization",
                "period": "2025-2026",
                "description": "<p>Managed a project team.</p>",
                "image": "img/project.png",
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            create_response.data["title"],
            "Project Manager",
        )
        self.assertEqual(
            create_response.data["description"],
            "Managed a project team.",
        )
        self.assertEqual(
            Experience.objects.count(),
            initial_count + 1,
        )

        new_id = create_response.data["id"]
        new_detail_url = reverse(
            "api:experience_detail",
            kwargs={"pk": new_id},
        )

        patch_response = self.client.patch(
            new_detail_url,
            {"period": "2026"},
            format="json",
        )
        self.assertEqual(
            patch_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(patch_response.data["period"], "2026")

        put_response = self.client.put(
            new_detail_url,
            {
                "title": "Project Manager",
                "institution": "Updated Organization",
                "period": "2026",
                "description": "Updated project description.",
                "image": "img/project.png",
            },
            format="json",
        )
        self.assertEqual(
            put_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            put_response.data["institution"],
            "Updated Organization",
        )

        delete_response = self.client.delete(new_detail_url)
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Experience.objects.filter(pk=new_id).exists()
        )

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        initial_count = Experience.objects.count()

        create_response = self.client.post(
            self.list_url,
            {
                "title": "Unauthorized Experience",
                "description": "Should not be created.",
            },
            format="json",
        )
        self.assertEqual(
            create_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            Experience.objects.count(),
            initial_count,
        )

        patch_response = self.client.patch(
            self.detail_url,
            {"title": "Updated by Editor"},
            format="json",
        )
        self.assertEqual(
            patch_response.status_code,
            status.HTTP_200_OK,
        )
        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.title,
            "Updated by Editor",
        )

        delete_response = self.client.delete(self.detail_url)
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Experience.objects.filter(
                pk=self.experience.pk
            ).exists()
        )

    def test_regular_user_and_anonymous_cannot_modify(self):
        initial_count = Experience.objects.count()
        original_title = self.experience.title

        # Anonymous user
        for response in [
            self.client.post(
                self.list_url,
                {"title": "Anonymous"},
                format="json",
            ),
            self.client.patch(
                self.detail_url,
                {"title": "Anonymous Update"},
                format="json",
            ),
            self.client.delete(self.detail_url),
            self.client.post(self.star_url),
        ]:
            self.assertIn(
                response.status_code,
                (
                    status.HTTP_401_UNAUTHORIZED,
                    status.HTTP_403_FORBIDDEN,
                ),
            )

        self.assertEqual(Experience.objects.count(), initial_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, original_title)

        # Regular user
        self.client.force_authenticate(user=self.regular_user)

        post_response = self.client.post(
            self.list_url,
            {"title": "Regular User"},
            format="json",
        )
        self.assertEqual(
            post_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        patch_response = self.client.patch(
            self.detail_url,
            {"title": "Unauthorized Update"},
            format="json",
        )
        self.assertEqual(
            patch_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        delete_response = self.client.delete(self.detail_url)
        self.assertEqual(
            delete_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Experience.objects.count(), initial_count)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, original_title)

    def test_star_requires_login_and_can_toggle(self):
        anonymous_response = self.client.post(self.star_url)

        self.assertIn(
            anonymous_response.status_code,
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
        )
        self.assertEqual(
            self.experience.starred_by.count(),
            0,
        )

        self.client.force_authenticate(user=self.regular_user)

        star_response = self.client.post(self.star_url)
        self.assertEqual(
            star_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertTrue(star_response.data["is_starred"])
        self.assertEqual(star_response.data["star_count"], 1)
        self.assertTrue(
            self.experience.starred_by.filter(
                pk=self.regular_user.pk
            ).exists()
        )

        unstar_response = self.client.post(self.star_url)
        self.assertEqual(
            unstar_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertFalse(unstar_response.data["is_starred"])
        self.assertEqual(unstar_response.data["star_count"], 0)

    def test_invalid_input_and_missing_experience(self):
        self.client.force_authenticate(user=self.owner)

        initial_count = Experience.objects.count()

        invalid_response = self.client.post(
            self.list_url,
            {
                "title": "<b></b>",
                "description": "Valid description",
            },
            format="json",
        )

        self.assertEqual(
            invalid_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            Experience.objects.count(),
            initial_count,
        )

        missing_url = reverse(
            "api:experience_detail",
            kwargs={
                "pk": "12345678-1234-5678-1234-567812345678"
            },
        )

        missing_response = self.client.get(missing_url)
        self.assertEqual(
            missing_response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_session_authentication_enforces_csrf(self):
        csrf_client = APIClient(enforce_csrf_checks=True)

        # Login menggunakan session authentication.
        login_success = csrf_client.login(
            username="owner_exp",
            password="password123",
        )
        self.assertTrue(login_success)

        # Request POST tanpa CSRF token harus ditolak.
        rejected_response = csrf_client.post(
            self.list_url,
            {
                "title": "CSRF Test",
                "description": "Testing CSRF protection.",
            },
            format="json",
        )

        self.assertEqual(
            rejected_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertFalse(
            Experience.objects.filter(title="CSRF Test").exists()
        )

        # Ambil halaman Experience untuk mendapatkan cookie CSRF.
        page_response = csrf_client.get(
            reverse("main:show_experience")
        )
        self.assertEqual(
            page_response.status_code,
            status.HTTP_200_OK,
        )

        csrf_token = csrf_client.cookies.get("csrftoken")
        self.assertIsNotNone(csrf_token)

        # Request dengan token CSRF harus berhasil.
        accepted_response = csrf_client.post(
            self.list_url,
            {
                "title": "CSRF Test",
                "description": "Testing CSRF protection.",
            },
            format="json",
            HTTP_X_CSRFTOKEN=csrf_token.value,
        )

        self.assertEqual(
            accepted_response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Experience.objects.filter(title="CSRF Test").exists()
        )
