from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available Tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve tags"""
        response = self.client.get(TAGS_URL)

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

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="Burger")
        Tag.objects.create(user=self.user, name="Souvlaki")

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test that tags returned belong to the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'niracainndeogecelo@aol.com',
            'ihatemyself'
        )
        Tag.objects.create(user=user2, name='Nira')
        tag = Tag.objects.create(user=self.user, name='Middle Eastern')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload eg a blank name"""
        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipes(self):
        """Test filtering only the tags that are assigned to recipes"""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Dinner')
        recipe = Recipe.objects.create(
            title='Egg, Spam, Sausage and Spam',
            time_minutes=15,
            price=5.00,
            user=self.user
        )
        recipe.tags.add(tag1)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, response.data)
        self.assertNotIn(serializer2.data, response.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tags by assigned returns unique items"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Lunch')
        recipe1 = Recipe.objects.create(
            title='Breakfast Burrito',
            time_minutes=20,
            price=6.00,
            user=self.user
        )
        recipe2 = Recipe.objects.create(
            title='Grilled Cheese Sandwich',
            time_minutes=5,
            price=2.00,
            user=self.user
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(response.data), 1)
