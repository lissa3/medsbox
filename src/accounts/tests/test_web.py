from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTest

from src.accounts.tests.factories.user_factory import UserFactory

User = get_user_model()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class AccountTest(WebTest):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.build()
        self.user_2 = UserFactory()
        self.url = reverse("account_signup")
        self.response = self.app.get(self.url)

    def test_signup_form(self):
        """UI for sign-up"""
        count_before = User.objects.count()

        self.assertEqual(self.response.status_code, 200)

        form = self.response.forms["signup_form"]
        form["username"] = self.user.username
        form["email"] = self.user.email
        form["password1"] = self.user.password
        form["password2"] = self.user.password
        form["agree_to_terms"] = True

        resp_post = form.submit()
        user_auth = User.objects.get(email=self.user.email)
        count_after = User.objects.count()

        self.assertEqual(resp_post.status_code, 302)
        self.assertIsNone(self.user.id)
        self.assertIsNotNone(user_auth.id)
        self.assertEqual(user_auth.email, self.user.email)
        self.assertNotEqual(count_before, count_after)
