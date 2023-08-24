from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from todo_list.models import Task, User, STATUSES


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.test_user = User(first_name='test', last_name='user', username='test_user', password='password123')
        self.test_user.save()
        self.test_task = Task.objects.create(title='test title 1', description='', status=STATUSES[0][0], user_id=self.test_user)
        Task.objects.create(title='test title 2', description='some description', status=STATUSES[1][0], user_id=self.test_user)
        Task.objects.create(title='test title 3', description='another description', status=STATUSES[1][0], user_id=self.test_user)

    def test_get_task_list(self):
        response = self.client.get(reverse('task-list'))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_task_list(self):
        response = self.client.get(reverse('user-task-list', args=(self.test_user.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task(self):
        response = self.client.get(reverse('task', args=(self.test_task.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.test_task.title)

    def test_create_task(self):
        sample_data = {
            'title': 'created test title',
            'description': '',
            'status': STATUSES[0][0],
            'user_id': self.test_user.id
        }
        response = self.client.post(reverse('create-task'), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_data['title'])

