from datetime import datetime, timezone

import factory
import factory.fuzzy
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker
from taggit.models import Tag

from src.accounts.tests.factories.user_factory import StaffUserFactory
from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker("word")
    icon = factory.django.ImageField()

    class Meta:
        model = Category

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        override default manager;
        create root categ without children;
        """
        # kwargs are {'name': 'leg', 'icon': <File: example.jpg>}
        return Category.add_root(**kwargs)


class PostFactory(DjangoModelFactory):
    author = factory.SubFactory(StaffUserFactory)
    published_at = fake.date_time(tzinfo=timezone.utc)
    status = factory.fuzzy.FuzzyChoice(Post.CurrentStatus.values)
    title = factory.Faker("word")
    content = factory.Faker("paragraph")
    # category = factory.SubFactory(Category) default

    class Meta:
        model = "posts.Post"

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.tags.add(*extracted)


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"tag {n}")
    slug = factory.LazyAttribute(lambda m: slugify(m.name))

    class Meta:
        model = Tag

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """create a  tag"""
        return Tag.objects.get_or_create({"name": elem} for elem in ["apple", "pier"])
