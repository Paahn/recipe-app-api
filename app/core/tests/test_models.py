from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'email@me.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email for a new user is normalized"""
        email = 'email@ME.COM'
        user = get_user_model().objects.create_user(
            email,
            'password12345'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """When creating user without email throw error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password12345')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'email@me.com',
            'password12345'
        )
        # the is_superuser field is included as part of the permissions mixins,
        # so we don't have to create a field for it in our model
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
