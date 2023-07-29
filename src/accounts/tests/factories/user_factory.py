import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from faker import Faker

User = get_user_model()

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda _: faker.unique.user_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.PostGenerationMethodCall("set_password", "12345abc")

    class Meta:
        model = User
        django_get_or_create = ("username", "email")


class AdminSupUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda _: faker.unique.user_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.PostGenerationMethodCall("set_password", "12345abc")
    is_staff = True
    is_superuser = True

    class Meta:
        model = User
        django_get_or_create = ("username", "email", "is_staff", "is_superuser")


class StaffUserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda _: faker.unique.user_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.PostGenerationMethodCall("set_password", "12345abc")
    is_staff = True
    is_superuser = False

    class Meta:
        model = User
        django_get_or_create = ("username", "email", "is_staff", "is_superuser")
