from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

# public user is an unauthenticated user, so anyone from the internet
# for example a new user to the site
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setup(self):
        self.client = APIClient()

    