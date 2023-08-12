from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from src.accounts.tests.factories import UserFactory
from src.contacts.exceptions import HtmxFailureError
from src.profiles.models import Profile
from src.profiles.tests.factories.profile_factory import ProfileFactory

User = get_user_model()


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class SubscribeTestCase(TestCase):
    def setUp(self) -> None:
        self.url = reverse("contacts:subscribe")

    def test_ok_subscription_news(self):
        """Auth-ed user can subscribe for a news letter"""
        user = UserFactory()
        self.client.force_login(user)
        profile = Profile.objects.get(user=user)
        headers = {"HTTP_HX-Request": "true"}
        resp = self.client.post(self.url, **headers)
        profile.refresh_from_db()

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.headers["HX-Redirect"])
        self.assertTrue(profile.want_news)

    def test_failed_subscription_news(self):
        """
        Failed subscription if not htmx request
        (no header htmx)
        """
        user = UserFactory()
        profile = user.profile
        self.client.force_login(user)
        with self.assertRaises(HtmxFailureError) as e:
            self.client.post(self.url)  # noqa

        profile.refresh_from_db()

        self.assertFalse(profile.want_news)
        self.assertEqual(str(e.exception), (_("Subscription failed")))

    def test_auth_user_get_subscr_page(self):
        user = UserFactory()
        self.client.force_login(user)
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)

    def test_Not_auth_user_no_subscr_page(self):
        client = Client()
        resp = client.get(self.url)
        self.assertEqual(resp.status_code, 302)


@override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
class UnSubscribeTestCase(TestCase):
    def test_ok_unsubscribe(self):
        """if profile exists -> via htmx unsubscribe successfull"""
        profile = ProfileFactory(want_news=True)
        headers = {"HTTP_HX-Request": "true"}
        url = reverse("contacts:end_news", kwargs={"uuid": profile.uuid})
        resp = self.client.post(url, **headers)
        profile.refresh_from_db()

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.headers["HX-Redirect"])
        self.assertFalse(profile.want_news)

    def test_failed_unsubscribe_no_htmx(self):
        """
        Failed un-subscribe if not htmx request
        (no header htmx)
        """
        profile = ProfileFactory(want_news=True)
        url = reverse("contacts:end_news", kwargs={"uuid": profile.uuid})

        with self.assertRaises(HtmxFailureError) as e:
            self.client.post(url)  # noqa
        self.assertTrue(profile.want_news)
        self.assertEqual(
            str(e.exception), (_("Something went wrong.Can't unsubscribe."))
        )

    def test_unsubscribe_page(self):
        """on GET request unsubscribe page if profile uuid in url"""
        profile = ProfileFactory(want_news=True)
        url = reverse("contacts:end_news", kwargs={"uuid": profile.uuid})

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
