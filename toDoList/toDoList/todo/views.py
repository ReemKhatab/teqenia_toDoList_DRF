from django.shortcuts import render
from .models import Task, Priority
from .serializer import TaskSerializer, PrioritySerializer
from datetime import timedelta
from datetime import datetime, timezone
from toDoList import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .utils.custompagination import CustomPagination

class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class=CustomPagination

    def get_queryset(self):
        
        return Task.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
       
        task = serializer.save()
        task.users.add(self.request.user)
        
    


class ToggleTodoStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    def patch(self, request, pk):
        try:
            todo = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({
                "message": "Task not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        todo.isCompleted = not todo.isCompleted
        todo.save()
        
        return Response({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "priority": todo.priority,
            "isCompleted": todo.isCompleted,
            "message": "Status toggled successfully"
        }, status=status.HTTP_200_OK)


class PriorityViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist() 
            access_token = request.headers.get('Authorization').split()[1]
            token = AccessToken(access_token)
            
            token.set_exp(from_time=datetime.now(),lifetime=timedelta(seconds=0)) 
           

            return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)