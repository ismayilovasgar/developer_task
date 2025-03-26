from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from .api.serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import status


@login_required(login_url="login_view")
def home(request):
    tasks = Task.objects.filter(user=request.user)
    context = {"tasks": tasks}
    return render(request, "home.html", context)


@api_view(["PATCH"])
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.user != request.user:
        raise PermissionDenied("Bu görevi güncelleme izniniz yok.")

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def create_task(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=403)

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save(user=request.user)
        return Response(TaskSerializer(task).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {"detail": "Task bulunamadı."}, status=status.HTTP_404_NOT_FOUND
        )

    # Kullanıcının sadece kendi görevini silmesine izin ver
    if task.user != request.user:
        raise PermissionDenied("Bu görevi silme izniniz yok.")

    # Task'ı sil
    task.delete()
    return Response(
        {"detail": "Task başarıyla silindi."}, status=status.HTTP_204_NO_CONTENT
    )


@api_view(["GET"])
def list_tasks(request):
    # İstifadəçi daxil olmamışsa, xəta veririk
    if not request.user.is_authenticated:
        raise PermissionDenied("Giriş etməlisiniz.")

    # URL-dən gələn 'status' parametrini alırıq
    status = request.GET.get(
        "status", None
    )  # Əgər 'status' parametri yoxdursa, None dəyəri alınır

    # Tapşırıqları istifadəçiyə aid olan, filtr edilmiş və ya bütün tapşırıqları əldə edirik
    if status:
        tasks = Task.objects.filter(user=request.user, status=status).order_by("status")
    else:
        tasks = Task.objects.filter(user=request.user).order_by("status")

    # Tapşırıqları serializ edirik
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
