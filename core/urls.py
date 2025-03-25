from django.contrib import admin
from django.urls import path, include
from task.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    ##
    ## <== API ==>
    path("api/v1/account/", include("account.api.urls")),
    path("api/v1/tasks/", include("task.api.urls")),
    ##
    ## <== Template ==>
    path("dashboard/", dashboard, name="dashboard"),
]
