from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/account/", include("account.api.urls")),
    path("api/v1/tasks/", include("task.api.urls")),
]
