from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from todo_list.models import Task, STATUSES
from .serializers import TaskSerializer, UserSerializer
from .filters import TaskFilter


#  -------------------------------------------------------------------------------------
#  CRUD operations
#  -------------------------------------------------------------------------------------
@api_view(['GET'])
def get_task_list(request):
    tasks = Task.objects.all()
    filter_set = TaskFilter(request.GET, queryset=tasks)
    if filter_set.is_valid():
        tasks = filter_set.qs
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_task_list(request, user_id):
    tasks = Task.objects.all().filter(user_id=user_id)
    filter_set = TaskFilter(request.GET, queryset=tasks)
    if filter_set.is_valid():
        tasks = filter_set.qs
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_id=request.user.id)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_id=request.user.id)
    task.delete()
    return Response(f'Task {task_id} successfully deleted', status=status.HTTP_200_OK)


#  -------------------------------------------------------------------------------------
#  Other API endpoints
#  -------------------------------------------------------------------------------------
@api_view(['POST'])
def mark_completed_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskSerializer(instance=task, data={'status': STATUSES['COMPLETED'][0]}, partial=True)
    if serializer.is_valid():
        serializer.update(instance=task, validated_data=serializer.validated_data)
    return Response(serializer.data, status=status.HTTP_200_OK)


#  -------------------------------------------------------------------------------------
#  Authorization
#  -------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([AllowAny,])
def signup(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
