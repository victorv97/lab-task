from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from todo_list.models import Task, User, STATUSES


class TaskAPITestCase(APITestCase):
    """
    Test API endpoints
    """

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
            Task.objects.create(title='test title 1', description='', status=STATUSES['NEW'][0], user_id=self.test_user),
            Task.objects.create(title='test title 2', description='', status=STATUSES['IN_PROGRESS'][0], user_id=self.test_user),
            Task.objects.create(title='test title 3', description='', status=STATUSES['COMPLETED'][0], user_id=self.test_user),
        )

        self.task_list_url = reverse('task-list')
        self.user_task_list_url = reverse('user-task-list', args=(self.test_user.id,))
        self.task_url = reverse('task', args=(self.test_tasks[0].id,))
        self.create_task_url = reverse('create-task')
        self.update_task_url = reverse('update-task', args=(self.test_tasks[1].id,))
        self.delete_task_url = reverse('delete-task', args=(self.test_tasks[2].id,))
        self.mark_task_url = reverse('mark-completed-task', args=(self.test_tasks[1].id,))

        self.login_url = reverse('token_obtain_pair')

        self.access_token = self.client.post(
            self.login_url,
            {
                'username': self.test_user.username,
                'password': password
            }
        ).data['access']

        self.auth_header = 'Bearer ' + self.access_token
        self.auth_header_fake = self.auth_header + 'fake'

    def test_get_task_list(self):
        """
        Test the access to all tasks list.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(self.task_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_task_list_unauthorized(self):
        """
        Test the access to all tasks list is forbidden for unauthorized users.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.get(self.task_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_task_list(self):
        """
        Test the endpoint returns all tasks of specified user.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(self.user_task_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_task_list_unauthorized(self):
        """
        Test the access to specified user's tasks list is forbidden for unauthorized users.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.get(self.user_task_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_task(self):
        """
        Test the endpoint returns information about a specified task.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(self.task_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.test_tasks[0].title)
        self.assertEqual(response.data['description'], self.test_tasks[0].description)
        self.assertEqual(response.data['status'], self.test_tasks[0].status)

    def test_get_task_unauthorized(self):
        """
        Test the access to specified task is forbidden for unauthorized users.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.get(self.task_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        """
        Test the endpoint creates a new Task and returns information about it.
        """
        sample_data = {
            'title': 'created test title',
            'description': '',
            'status': STATUSES['NEW'][0],
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
        """
        Test the access to task creation is forbidden for unauthorized users.
        """
        sample_data = {
            'title': 'created test title by unauthorized',
            'description': '',
            'status': STATUSES['NEW'][0],
            'user_id': self.test_user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.post(self.create_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task(self):
        """
        Test the endpoint updates the specified task and returns information about it.
        """
        sample_data = {
            'title': 'updated test title',
            'description': 'updated description',
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post(self.update_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], sample_data['title'])
        self.assertEqual(response.data['description'], sample_data['description'])

    def test_update_task_unauthorized(self):
        """
        Test the access to task update is forbidden for unauthorized users.
        """
        sample_data = {
            'title': 'updated test title by unauthorized',
            'description': 'updated description',
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.post(self.update_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_not_found(self):
        """
        Test the access to task update is forbidden for other authenticated users.
        """
        sample_data = {
            'title': 'updated test title by other user',
            'description': 'updated description',
        }
        other_user = User.objects.create_user(
            first_name='other',
            last_name='user',
            username='other_user',
            password='password123456'
        )
        other_access_token = self.client.post(
            self.login_url,
            {
                'username': 'other_user',
                'password': 'password123456'
            }
        ).data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + other_access_token)
        response = self.client.post(self.update_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task(self):
        """
        Test the endpoint deletes the specified task by authenticated owner only.
        """
        other_user = User.objects.create_user(
            first_name='other 2',
            last_name='user',
            username='other_user_2',
            password='password123456'
        )
        other_access_token = self.client.post(
            self.login_url,
            {
                'username': 'other_user_2',
                'password': 'password123456'
            }
        ).data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + other_access_token)
        response = self.client.delete(self.delete_task_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.delete(self.delete_task_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.delete(self.delete_task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_completed_task(self):
        """
        Test the endpoint updates the specified task status as COMPLETED.
        """
        sample_data = {}
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post(self.mark_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], STATUSES['COMPLETED'][0])

    def test_mark_completed_task_unauthorized(self):
        """
        Test the access to task update is forbidden for unauthorized users.
        """
        sample_data = {}
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header_fake)
        response = self.client.post(self.mark_task_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_by_status(self):
        """
        Test the endpoint filters the task list by each status.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        for status_key in STATUSES:
            status_val = STATUSES[status_key][0]
            response = self.client.get(self.task_list_url + f'?status={status_val}')
            queryset = Task.objects.all().filter(status=status_val)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), len(queryset))


class AuthAPITestCase(APITestCase):
    """
    Test authorization API endpoints
    """

    def setUp(self):
        self.password = 'password123'
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            first_name='test',
            last_name='user',
            username='test_auth_user',
            password=self.password
        )

        self.login_url = reverse('token_obtain_pair')
        self.signup_url = reverse('signup')
        self.refresh_url = reverse('token_refresh')

    def test_login(self):
        """
        Test the endpoint returns a pair of JWT tokens with access and refresh fields.
        """
        response = self.client.post(
            self.login_url,
            {
                'username': self.test_user.username,
                'password': self.password
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_signup(self):
        """
        Test the endpoint creates a new User with hashed password.
        """
        sample_data = {
            'first_name': 'some',
            'last_name': 'user',
            'username': 'test_some_user',
            'password': 'password12'
        }
        response = self.client.post(self.signup_url, sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], sample_data['first_name'])
        self.assertEqual(response.data['last_name'], sample_data['last_name'])
        self.assertEqual(response.data['username'], sample_data['username'])
        self.assertNotEquals(response.data['password'], sample_data['password'])

    def test_refresh(self):
        """
        Test the endpoint returns a new access token with by sending refresh token.
        """
        response_token = self.client.post(
            self.login_url,
            {
                'username': self.test_user.username,
                'password': self.password
            }
        )
        refresh_token = {'refresh': response_token.data['refresh']}

        response = self.client.post(self.refresh_url, refresh_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

