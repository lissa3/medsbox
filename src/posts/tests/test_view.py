from django.test import Client, TestCase, override_settings
from django.urls import reverse

from src.accounts.tests.factories import StaffUserFactory, UserFactory
from src.posts.models.post_model import Post

from .factories import PostFactory


class PostListTestCase(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.staff = StaffUserFactory()
        self.posts_public = PostFactory.create_batch(
            10, status=Post.CurrentStatus.PUB.value
        )
        self.posts_drafts = PostFactory.create_batch(
            2, status=Post.CurrentStatus.DRAFT.value
        )
        self.client = Client()

    @override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
    def test_view_public_posts_ru(self):
        """show only public posts; lang ru in url path"""
        path = reverse("posts:post_list")
        lang = path.split("/")[1]
        response = self.client.get(path)

        posts_count = Post.objects.get_public().count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(posts_count, 10)
        self.assertEqual("ru", lang)
        self.assertEqual(
            response.context_data["paginator"].count, Post.objects.get_public().count()
        )

    @override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
    def test_public_posts_en(self):
        """show only public posts; lang en in url path"""
        path = reverse("posts:post_list")
        lang = path.split("/")[1]
        response = self.client.get(path)
        posts_count = Post.objects.get_public().count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual("en", lang)
        self.assertEqual(posts_count, 10)
        self.assertEqual(
            response.context_data["paginator"].count, Post.objects.get_public().count()
        )
