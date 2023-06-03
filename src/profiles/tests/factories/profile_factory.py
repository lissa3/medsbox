import factory

from src.accounts.tests.factories.user_factory import UserFactory
from src.profiles.models import Profile


class ProfileFactory(factory.django.DjangoModelFactory):
    # created_at; updated_at
    user = factory.SubFactory(UserFactory)
    avatar = factory.django.ImageField()

    class Meta:
        model = Profile
        django_get_or_create = ("user",)
