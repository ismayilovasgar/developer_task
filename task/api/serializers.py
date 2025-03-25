# serializers.py
from ..models import Task
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    user = serializers.StringRelatedField() 
    created_at_pretty = serializers.SerializerMethodField()
    updated_at_pretty = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id","title","content","status","status_display","user","created_at_pretty","updated_at_pretty",]

    def get_status_display(self, obj):
        return obj.get_status_display()# Modeldeki get_status_display() metodunu çağırıyoruz

    def get_created_at_pretty(self, obj):
        return self.pretty_date(obj.created_at)

    def get_updated_at_pretty(self, obj):
        return self.pretty_date(obj.updated_at)

    def pretty_date(self, value):
        if not isinstance(value, datetime.datetime):
            return value

        value = timezone.localtime(value) 

        today = timezone.localtime(timezone.now()).date()
        date_value = value.date()

        if date_value == today:
            return f"Bugün {value.strftime('%H:%M')}"
        elif date_value == today - datetime.timedelta(days=1):
            return f"Dünən {value.strftime('%H:%M')}"
        else:
            return value.strftime("%d.%m.%Y") 
        
        
    # def pretty_date(self, value):
    #     """ Tarihi 'Bugün', 'Dünən' formatına çevirir. """
    #     if not isinstance(value, datetime.datetime):
    #         return value

    #     value = timezone.localtime(value)  # Saat farkını düzeltir
    #     today = timezone.localtime(timezone.now()).date()
    #     date_value = value.date()

    #     if date_value == today:
    #         return f"Bugün {value.strftime('%H:%M')}"
    #     elif date_value == today - datetime.timedelta(days=1):
    #         return f"Dünən {value.strftime('%H:%M')}"
    #     else:
    #         return value.strftime("%d.%m.%Y")
