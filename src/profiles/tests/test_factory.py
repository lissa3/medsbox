import pytest

from src.profiles.tests.factories.profile_factory import ProfileFactory


@pytest.mark.django_db
class TestProfile:
    def test_factory(self):
        profile = ProfileFactory()
        assert profile is not None
        assert profile.user is not None
