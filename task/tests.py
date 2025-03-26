from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from task.models import Task


class TaskTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "content": "This is a test task.",
            "status": "pending",
        }
        response = self.client.post("/api/v2/tasks/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["content"], data["content"])

    def test_create_task_unauthenticated(self):
        self.client.logout()  # Çıkış yapıyoruz
        data = {
            "title": "Test Task",
            "content": "This is a test task.",
            "status": "pending",
        }
        response = self.client.post("/api/v2/tasks/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task(self):
        task = Task.objects.create(
            title="Test Task",
            content="This is a test task.",
            status="pending",
            user=self.user,
        )
        data = {"status": "completed"}
        response = self.client.patch(f"/api/v2/tasks/update/{task.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_update_task_permission_denied(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser", email="otheruser@example.com", password="password123"
        )
        self.client.login(
            username="otheruser", password="password123"
        )  # Farklı bir kullanıcıyla giriş yapıyoruz
        task = Task.objects.create(
            title="Test Task",
            content="This is a test task.",
            status="pending",
            user=self.user,
        )
        data = {"status": "completed"}
        response = self.client.patch(f"/api/v2/tasks/update/{task.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        task = Task.objects.create(
            title="Test Task",
            content="This is a test task.",
            status="pending",
            user=self.user,
        )
        response = self.client.delete(f"/api/v2/tasks/delete/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=task.id).count(), 0)

    def test_delete_task_permission_denied(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser", email="otheruser@example.com", password="password123"
        )
        self.client.login(username="otheruser", password="password123")
        task = Task.objects.create(
            title="Test Task",
            content="This is a test task.",
            status="pending",
            user=self.user,
        )
        response = self.client.delete(f"/api/v2/tasks/delete/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tasks(self):
        Task.objects.create(
            title="Test Task 1",
            content="This is the first test task.",
            status="pending",
            user=self.user,
        )
        Task.objects.create(
            title="Test Task 2",
            content="This is the second test task.",
            status="completed",
            user=self.user,
        )
        response = self.client.get("/api/v2/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_tasks_unauthenticated(self):
        self.client.logout()  # Çıkış yapıyoruz
        response = self.client.get("/api/v2/tasks/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tasks_with_status_filter(self):
        Task.objects.create(
            title="Test Task 1",
            content="This is the first test task.",
            status="pending",
            user=self.user,
        )
        Task.objects.create(
            title="Test Task 2",
            content="This is the second test task.",
            status="completed",
            user=self.user,
        )
        response = self.client.get("/api/v2/tasks/?status=pending")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "pending")
