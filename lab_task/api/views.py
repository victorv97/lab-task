from rest_framework.response import Response
from rest_framework.decorators import api_view
from todo_list.models import Task


@api_view(['GET'])
def get_task_list(request):
    # TODO: retrieve data, serialize
    data = {1: '1', 2: '1'}
    return Response(data)
