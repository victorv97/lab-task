from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from todo_list.models import Task, User, STATUSES


class TaskAPITestCase(APITestCase):

    def setUp(self):
        password = 'password123'
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            first_name='test',
            last_name='user',
            username='test_user',
            password=password
        )

        self.test_tasks = (
            Task.objects.create(title='test title 1', description='', status=STATUSES[0][0], user_id=self.test_user),
            Task.objects.create(title='test title 2', description='', status=STATUSES[1][0], user_id=self.test_user),
            Task.objects.create(title='test title 3', description='', status=STATUSES[2][0], user_id=self.test_user),
        )

        self.task_list_url = reverse('task-list')
        self.user_task_list_url = reverse('user-task-list', args=(self.test_user.id,))
        self.task_url = reverse('task', args=(self.test_tasks[0].id,))
        self.create_task_url = reverse('create-task')
        self.login_url = reverse('token_obtain_pair')

        self.access_token = self.client.post(
            self.login_url,
            {
                'username': self.test_user.username,
                'password': password
            }
        ).data['access']

        self.auth_header = 'Bearer ' + self.access_token
        self.auth_header_fake = 'fake'

    def test_get_task_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(self.task_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_list_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.get(self.task_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_task_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(self.user_task_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_task_list_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.get(self.user_task_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_task(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(self.task_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.test_tasks[0].title)

    def test_get_task_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.get(self.task_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        sample_data = {
            'title': 'created test title',
            'description': '',
            'status': STATUSES[0][0],
            'user_id': self.test_user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post(self.create_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_data['title'])
        self.assertEqual(response.data['description'], sample_data['description'])
        self.assertEqual(response.data['status'], sample_data['status'])
        self.assertEqual(response.data['user_id'], sample_data['user_id'])

    def test_create_task_task_unauthorized(self):
        sample_data = {
            'title': 'created test title',
            'description': '',
            'status': STATUSES[0][0],
            'user_id': self.test_user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.post(self.create_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
