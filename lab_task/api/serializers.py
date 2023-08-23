from rest_framework import serializers
from todo_list.models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

