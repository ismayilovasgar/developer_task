from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


# Create your views here.
def home(request):
    user = None
    auth = JWTAuthentication()

    # Token doğrulama
    try:
        header = request.META.get('HTTP_AUTHORIZATION')
        if header and header.startswith('Bearer '):
            token = header.split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
    except AuthenticationFailed:
        user = None

    return render(request, "home.html", {"jwt_user": user})
  
def login(request):
    user = None
    auth = JWTAuthentication()

    # Token doğrulama
    try:
        header = request.META.get('HTTP_AUTHORIZATION')
        if header and header.startswith('Bearer '):
            token = header.split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
    except AuthenticationFailed:
        user = None

    return render(request, "login.html", {"jwt_user": user})