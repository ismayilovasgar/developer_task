from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from ..models import Task
from .serializers import TaskSerializer
from rest_framework.exceptions import PermissionDenied


class TaskFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Task.STATUS_CHOICES)

    class Meta:
        model = Task
        fields = ["status"]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = TaskFilter
    ordering_fields = ["title", "status"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Yalnızca giriş etmiş istifadəçinin tapşırıqlarını qaytarır.
        """
        return Task.objects.filter(user=self.request.user)
        # return Task.objects.all()

    def perform_create(self, serializer):
        """
        Tapşırıq yaradılarkən istifadəçi məlumatını da saxlayır.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Tapşırıq yenilənərkən, yalnızca həmin istifadəçinin tapşırıqları yenilənə bilər.
        """
        task = self.get_object()
        if task.user != self.request.user:
            raise PermissionDenied("Bu tapşırığı yeniləmək üçün icazəniz yoxdur.")
        serializer.save()

    def perform_patch(self, serializer):
        """
        Tapşırıq qismən yenilənərkən, yalnızca həmin istifadəçinin tapşırıqları yenilənə bilər.
        """
        task = self.get_object()
        if task.user != self.request.user:
            raise PermissionDenied("Bu tapşırığı yeniləmək üçün icazəniz yoxdur.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Tapşırıq silinərkən, yalnızca həmin istifadəçi öz tapşırığını silə bilər.
        """
        if instance.user != self.request.user:
            raise PermissionDenied("Bu tapşırığı silmək üçün icazəniz yoxdur.")
        instance.delete()
