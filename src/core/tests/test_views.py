from django.urls import reverse

from src.core.views import home


class TestHome:
    def test_unauth_home(self, client):
        """Not auth user gets home page"""
        resp = client.get(reverse("home"))
        assert resp.status_code == 200

    def test_unaut_intro(self, client):
        """Not auth user gets intro page"""
        resp = client.get(reverse("core:intro"))
        assert resp.status_code == 200
