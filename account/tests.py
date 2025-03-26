from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):
    def test_register_view(self):
        url = reverse("register_view")
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(url, data)

        if response.status_code == 200:
            print(response.context["form"].errors)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login_view(self):
        user = User.objects.create_user(
            username="test", email="test@example.com", password="strongpassword123"
        )
        url = reverse("login_view")
        data = {
            "username": "test",
            "password": "strongpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home_page"))

    def test_logout_view(self):
        # İstifadəçini yaradırıq
        user = User.objects.create_user(
            username="test", email="test@example.com", password="strongpassword123"
        )
        # İstifadəçini daxil edirik
        self.client.login(username="test", password="strongpassword123")

        # Logout endpoint-ə request atırıq
        url = reverse("logout_view")
        response = self.client.get(url)

        # Debug üçün print əlavə edək
        print(f"Logout Response: {response.status_code}, Redirect URL: {response.url}")

        # 302 Redirect olmalıdır
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_view"))
