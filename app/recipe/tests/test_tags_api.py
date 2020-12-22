from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URLS = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    """Test the pubclicly available Tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve tags"""
        response = self.client.get(TAGS_URLS)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'aladeen@aladeen.wa',
            'aladeen'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)