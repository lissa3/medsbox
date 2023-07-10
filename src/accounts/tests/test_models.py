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

    def test_user_delete(self):
        """when user deleted -> their profiles deleted as well"""
        user_inital_count = User.objects.count()
        profile_inital_count = Profile.objects.count()
        self.user.delete()
        user_final_count = User.objects.count()
        profile_final_count = Profile.objects.count()

        self.assertEqual(user_inital_count, 1)
        self.assertEqual(user_inital_count, profile_inital_count)
        self.assertEqual(user_final_count, 0)
        self.assertEqual(user_final_count, profile_final_count)
