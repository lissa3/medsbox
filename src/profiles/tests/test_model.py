import time_machine
from django.test import TestCase

from src.accounts.tests.factories.user_factory import UserFactory
from src.profiles.models import Profile


class UserTestCase(TestCase):
    @time_machine.travel("2023-01-01")
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client.login(email=self.user.email, password="secret")

    def test_user_attributes(self):
        """test forming profile via signal when new user created"""
        profile = Profile.objects.get(user=self.user)

        self.assertEqual(profile.user.banned, False)
        self.assertEqual(profile.info, "")
        self.assertEqual(profile.avatar, "")
        self.assertFalse(profile.user.blackListEmail, False)
        self.assertTrue(profile.created_at, "2023-01-01")

    def test_user_delete(self):
        """when user deleted profile deleted too"""
        self.user.delete()

        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=self.user)

    def test_profile_delete(self):
        """when profile deleted user becomes inactive"""
        self.user.profile.delete()

        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=self.user.profile.id)
        self.assertFalse(self.user.is_active)
