from django.contrib.auth import get_user_model
from django.test import TestCase

from src.profiles.models import Profile

from .factories.user_factory import UserFactory

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_user_attributes(self):
        """test forming profile via signal when new user created"""
        user = User.objects.last()
        profile = Profile.objects.last()

        self.assertEqual(user.email, self.user.email)
        self.assertTrue(self.user.profile.id, profile.id)
        self.assertFalse(self.user.blackListEmail, False)
