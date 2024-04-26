from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.test_user = get_user_model().objects.create_user(username='admin', password='admin')

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'url')

    def test_login_fail(self):
        response = self.client.post(self.login_url, {'username': 'admin1', 'password': 'admin1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Invalid username or password.', status_code=400)
