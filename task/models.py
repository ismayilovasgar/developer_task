from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import CustomUser


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Gözləyir"),
        ("completed", "Tamamlandı"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=50)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def __str__(self):
        return self.title
