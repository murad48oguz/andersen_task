from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def test_registration_success(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'securepassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_registration_missing_first_name(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'securepassword123',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    def test_registration_weak_password(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': '123',
            'first_name': 'Test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='securepassword123',
            first_name='Test'
        )
    
    def test_login_success(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'securepassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)