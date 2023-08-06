from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest

from src.accounts.tests.factories import UserFactory

User = get_user_model()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class SubscribeLinkTest(WebTest):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.url = reverse("home")

    def test_auth_user_has_subscr_link_in_menu(self):
        """Auth user has link to subscribe for a newsletter"""
        self.app.set_user(self.user)
        self.response = self.app.get(self.url)
        self.assertEqual(self.response.status_code, 200)

        subs_link = self.response.html.find("a", id="subLink")

        self.assertIsNotNone(subs_link)

    def test_unauth_user_no_link_in_menu(self):
        """Unauth used - no link in menu to subscribe for a newsletter"""

        self.response = self.app.get(self.url)
        self.assertEqual(self.response.status_code, 200)

        subs_link = self.response.html.find("a", id="subLink")

        self.assertIsNone(subs_link)
