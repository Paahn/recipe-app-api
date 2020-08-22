from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


# public user is an unauthenticated user, so anyone from the internet
# for example a new user to the site
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setup(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'erranmorrad@yalla.com',
            'password': 'yalla',
            'name': 'Erran Morrad'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test that creating an existing user fails"""
        payload = {
            'email': 'erranmorrad@yalla.com',
            'password': 'yalla',
            'name': 'Erran Morrad'
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password is more than 5 characters"""
        payload = {
            'email': 'erranmorrad@yalla.com',
            'password': 'oug',
            'name': 'OMG whiz'
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a user token is created"""
        payload = {
            'email': 'erranmorrad@yalla.com',
            'password': 'oug',
            'name': 'OMG whiz'
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='erranmorrad@yalla.com', password='oug')
        payload = {
            'email': 'erranmorrad@yalla.com',
            'password': 'ooog',
            'name': 'OMG whiz'
        }
        response = self.client.post(TOKEN_URL, payload)

        