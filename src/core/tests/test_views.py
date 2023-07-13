from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(LANGUAGE_CODE="uk", LANGUAGES=(("uk", "Ukrainian"),))
class CategsTempTagsTest(TestCase):
    """test home and intro view"""

    def test_home_page(self):
        """home"""
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_intro_page(self):
        """intro; tempor rendering catges here"""
        url = reverse("core:intro")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
