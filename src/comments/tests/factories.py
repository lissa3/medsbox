import factory

from src.accounts.models import User
from src.comments.models import Comment
from src.posts.models.post_model import Post


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    body = factory.Faker("sentence")
    post = factory.SubFactory(Post)
    user = factory.SubFactory(User)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        override default manager;
        create root comment without children;
        """
        return Comment.add_root(**kwargs)
