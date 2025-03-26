
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Task
from ..api.serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import status



@api_view(["PATCH"])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {"detail": "Tapşırıq tapılmadı."}, status=status.HTTP_404_NOT_FOUND
        )

    if task.user != request.user:
        raise PermissionDenied("Bu tapşırığı yeniləməyə icazəniz yoxdur.")

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def create_task(request):
    if not request.user.is_authenticated:
        return Response({"detail": "İlk öncə daxil olun."}, status=403)

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
            {"detail": "Tapşırıq tapılmadı."}, status=status.HTTP_404_NOT_FOUND
        )

    if task.user != request.user:
        raise PermissionDenied("Bu tapşırığı silməyə icazəniz yoxdur.")

    task.delete()
    return Response(
        {"detail": "Tapşırıq uğurla silindi."}, status=status.HTTP_204_NO_CONTENT
    )


@api_view(["GET"])
def list_tasks(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("Daxil olmalısınız.")

    status = request.GET.get("status", None)
    if status:
        tasks = Task.objects.filter(user=request.user, status=status).order_by("status")
    else:
        tasks = Task.objects.filter(user=request.user).order_by("status")

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


## <======= API V1 ## =======>
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.filters import OrderingFilter
# from django_filters import rest_framework as filters
# from ..models import Task
# from .serializers import TaskSerializer
# from rest_framework.exceptions import PermissionDenied

# class TaskFilter(filters.FilterSet):
#     status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)

#     class Meta:
#         model = Task
#         fields = ["status"]


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
#     filterset_class = TaskFilter
#     ordering_fields = ["title", "status"]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """
#         Yalnızca giriş etmiş istifadəçinin tapşırıqlarını qaytarır.
#         """
#         return Task.objects.filter(user=self.request.user).order_by("status")
#         # return Task.objects.all()

#     def perform_create(self, serializer):
#         """
#         Tapşırıq yaradılarkən istifadəçi məlumatını da saxlayır.
#         """
#         serializer.save(user=self.request.user)

#     def perform_update(self, serializer):
#         """
#         Tapşırıq yenilənərkən, yalnızca həmin istifadəçinin tapşırıqları yenilənə bilər.
#         """
#         task = self.get_object()
#         if task.user != self.request.user:
#             raise PermissionDenied("Bu tapşırığı yeniləmək üçün icazəniz yoxdur.")
#         serializer.save()

#     def perform_patch(self, serializer):
#         """
#         Tapşırıq qismən yenilənərkən, yalnızca həmin istifadəçinin tapşırıqları yenilənə bilər.
#         """
#         task = self.get_object()
#         if task.user != self.request.user:
#             raise PermissionDenied("Bu tapşırığı yeniləmək üçün icazəniz yoxdur.")
#         serializer.save()

#     def perform_destroy(self, instance):
#         """
#         Tapşırıq silinərkən, yalnızca həmin istifadəçi öz tapşırığını silə bilər.
#         """
#         if instance.user != self.request.user:
#             raise PermissionDenied("Bu tapşırığı silmək üçün icazəniz yoxdur.")
#         instance.delete()
