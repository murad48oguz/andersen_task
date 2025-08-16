from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "user"]
        read_only_fields = ["user"]

    def validate_status(self, value):
        value = value.lower()
        valid_statuses = ["new", "in_progress", "completed"]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}")
        return value
