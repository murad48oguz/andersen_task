from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='securepassword123',
            first_name='Test'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='securepassword123',
            first_name='Other'
        )
        
        self.task1 = Task.objects.create(
            title='Task 1',
            description='Description 1',
            status='new',
            user=self.user
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Description 2',
            status='in_progress',
            user=self.user
        )
        self.task3 = Task.objects.create(
            title='Task 3',
            status='completed',
            user=self.user
        )
        self.other_task = Task.objects.create(
            title='Other Task',
            user=self.other_user
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        
    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'new'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 5)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['status'], 'new')

    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')

    def test_retrieve_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        data = {'title': 'Updated Task', 'status': 'in_progress'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')
        self.assertEqual(self.task1.status, 'in_progress')

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 3)

    def test_access_other_users_task(self):
        url = reverse('task-detail', kwargs={'pk': self.other_task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_other_users_task(self):
        url = reverse('task-detail', kwargs={'pk': self.other_task.id})
        data = {'title': 'Hacked Task'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
    def test_filter_by_status_new(self):
        url = reverse('task-list') + '?status=new'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'new')

    def test_filter_by_status_completed(self):
        url = reverse('task-list') + '?status=completed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'completed')

    def test_invalid_status_filter(self):
        url = reverse('task-list') + '?status=invalid'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_mark_completed_action(self):
        url = reverse('task-mark-as-completed', kwargs={'pk': self.task1.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'completed')

    def test_my_tasks_action(self):
        url = reverse('task-my-tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_invalid_status_update(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        data = {'status': 'invalid_status'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_create_task_invalid_status(self):
        url = reverse('task-list')
        data = {'title': 'Invalid Task', 'status': 'wrong_status'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_pagination(self):
        for i in range(15):
            Task.objects.create(title=f'Task {i+4}', user=self.user)
            
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # PAGE_SIZE = 10
        self.assertIsNotNone(response.data['next'])