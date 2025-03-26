from django.contrib import admin
from django.urls import path, include
from task.views import *
from account.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    ##
    ## <== API ==>
    path("api/v1/account/", include("account.api.urls")),
    path("api/v1/tasks/", include("task.api.urls")),
    path("api/v2/tasks/", include("task.urls")),
    ##
    ## <== Template ==>
    path("", home, name="home_page"),
    path("login/", login_view, name="login_view"),
    path("register/", register_view, name="register_view"),
    path("logout/", logout_view, name="logout_view"),
]
