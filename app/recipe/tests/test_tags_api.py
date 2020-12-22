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