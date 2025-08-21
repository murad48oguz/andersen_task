from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner
from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidStatusError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid status parameter. Valid values are: new, in_progress, completed.'
    default_code = 'invalid_status'


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
    
        status_param = self.request.query_params.get("status")
        if status_param:
            status_param = status_param.lower()
            valid_statuses = ["new", "in_progress", "completed"]
            
            if status_param not in valid_statuses:
                return queryset.none()
                
            queryset = queryset.filter(status=status_param)
        
        return queryset

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='my-tasks')
    def my_tasks(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], url_path='mark-completed')
    def mark_as_completed(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
