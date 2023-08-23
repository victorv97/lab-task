from rest_framework.response import Response
from rest_framework.decorators import api_view
from todo_list.models import Task, User
from .serializers import TaskSerializer


@api_view(['GET'])
def get_task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_task_list(request, user_id):
    tasks = Task.objects.all().filter(user_id=user_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_task(request, task_id):
    tasks = Task.objects.all().filter(id=task_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return Response(f'Task {task_id} successfully deleted')
