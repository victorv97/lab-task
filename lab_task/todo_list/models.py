from django.db import models


STATUSES = (
    (0, 'New'),
    (1, 'In Progress'),
    (2, 'Completed'),
)


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.TextField(max_length=64, blank=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=False)
    status = models.IntegerField(choices=STATUSES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
