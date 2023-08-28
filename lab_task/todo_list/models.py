from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator


STATUSES = {
    'NEW': (0, 'New'),
    'IN_PROGRESS': (1, 'In Progress'),
    'COMPLETED': (2, 'Completed'),
}


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=32, blank=False)
    last_name = models.TextField(max_length=64, blank=True)
    username = models.CharField(max_length=32, unique=True, blank=False)
    password = models.CharField(
        max_length=128,
        blank=False,
        validators=[
            MinLengthValidator(6, 'The field must contain at least 6 characters')
        ]
    )
    objects = UserManager()


class Task(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=1024, blank=True)
    status = models.IntegerField(choices=tuple(STATUSES.values()))
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
