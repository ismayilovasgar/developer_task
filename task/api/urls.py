#
## <======= API V2 =========>
from django.urls import path
from .views import *


urlpatterns = [
    path("", list_tasks, name="list_tasks"),                         # Bütün tapşırıqları siyahıla
    path("create/", create_task, name="create_task"),                # Yeni tapşırıq yarat
    path("update/<int:task_id>/", update_task, name="update_task"),  # Tapşırığı yenilə
    path("delete/<int:task_id>/", delete_task, name="delete_task"),  # Tapşırığı sil
]

## <======= API V1=======>----------------------------------------------------------------
# # task/api/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet

# router = DefaultRouter()
# router.register(r'', TaskViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
