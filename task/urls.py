# task/api/urls.py
from django.urls import path, include
from .views import *


urlpatterns = [
    path("", list_tasks, name="list_tasks"),  # Tüm görevleri listele
    path("create/", create_task, name="create_task"),  # Yeni görev oluştur
    path("update/<int:task_id>/", update_task, name="update_task"),  # Görev güncelle
    path("delete/<int:task_id>/", delete_task, name="delete_task"),  # Görev sil
]
