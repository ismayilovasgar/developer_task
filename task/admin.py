from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "user__email")  
    ordering = ("-created_at",)