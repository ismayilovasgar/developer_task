from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required
from task.models import Task

# Create your views here.


@login_required(login_url="login_view")
def home(request):

    tasks = Task.objects.filter(user=request.user)

    context = {"tasks": tasks}

    return render(request, "home.html", context)


# @login_required(login_url="login_view")
# def home(request):
#     user = None
#     auth = JWTAuthentication()

#     # Token doğrulama
#     try:
#         header = request.META.get('HTTP_AUTHORIZATION')
#         if header and header.startswith('Bearer '):
#             token = header.split(' ')[1]
#             validated_token = auth.get_validated_token(token)
#             user = auth.get_user(validated_token)
#     except AuthenticationFailed:
#         user = None

#     return render(request, "home.html", {"jwt_user": user})


def login(request):
    user = None
    auth = JWTAuthentication()

    # Token doğrulama
    try:
        header = request.META.get("HTTP_AUTHORIZATION")
        if header and header.startswith("Bearer "):
            token = header.split(" ")[1]
            validated_token = auth.get_validated_token(token)
            user = auth.get_user(validated_token)
    except AuthenticationFailed:
        user = None

    return render(request, "login.html", {"jwt_user": user})
