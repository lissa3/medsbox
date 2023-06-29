from datetime import datetime, timezone

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from src.posts.models.categ_model import Category

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
        return Category.add_root(**kwargs)


# class PostFactory(DjangoModelFactory):
#     # author = factory.StubFactory(StaffUserFactory)
#     # published_at = fake.date_time(tzinfo=timezone.utc)
#     published_at = factory.LazyFunction(datetime.today)
#     # status = factory.fuzzy.FuzzyChoice(Post.CurrentStatus.values)

#     # content = factory.Faker("paragraph")
#     # title = factory.Faker()
#     # content = factory.Faker()

#     class Meta:
#         model = "posts.Post"
