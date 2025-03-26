from django.contrib.auth.decorators import login_required
from .models import Task
from django.shortcuts import render
''

@login_required(login_url="login_view")
def home(request):
    tasks = Task.objects.filter(user=request.user)
    context = {"tasks": tasks}
    return render(request, "home.html", context)
