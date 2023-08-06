from src.profiles.models import Profile
from src.profiles.tests.factories.profile_factory import ProfileFactory


class TestProfile:
    def test_factory(self):
        profile = ProfileFactory()

        assert profile is not None
        assert profile.user is not None

    def test_users_wanted_news(self):
        """manager returns active users who want to get news via email"""
        profile_1 = ProfileFactory(want_news=True)
        user = profile_1.user
        user.is_active = False
        user.save()
        ProfileFactory(want_news=True)
        ProfileFactory(want_news=True)
        ProfileFactory(want_news=True)

        assert 3 == Profile.objects.send_news().count()
