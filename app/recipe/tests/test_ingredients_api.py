from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientsApiTests(TestCase):
  """Test the publicly available ingredients API"""

  def setUp(self):
    self.client = APIClient()

  def test_login_required(self):
    """Test that login is required to access this endpoint"""
    response = self.client.get(INGREDIENTS_URL)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
  """Test the private ingredients API"""

  def setUp(self):
    self.client = APIClient()
    self.user = get_user_model().objects.create_user(
      'borat@verynice.kz',
      'pamelasmallerthan3'
    )
    self.client.force_authenticate(self.user)

  def test_retrieve_ingredients_list(self):
    """Test retrieving a list of ingredients for an authenticated user"""
    Ingredient.objects.create(user=self.user, name='A very nice potato')
    Ingredient.objects.create(user=self.user, name='Wife milk cheese')

    response = self.client.get(INGREDIENTS_URL)

    ingredients = Ingredient.objects.all().order_by('-name')
    serializer = IngredientSerializer(ingredients, many=True)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, serializer.data)
