from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView,CustomLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), 
    path("login/", CustomLoginView.as_view(), name="login"), 
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), 
]