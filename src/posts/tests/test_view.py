from django.test import Client, TestCase, override_settings
from django.urls import reverse

from src.accounts.tests.factories import StaffUserFactory, UserFactory
from src.comments.tests.factories import CommentFactory
from src.posts.models.categ_model import Category
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


class PostCategsTestCase(TestCase):
    def setUp(self) -> None:
        self.categ_root_1 = Category.add_root(name="parent1")
        self.categ_root_2 = self.categ_root_1.add_sibling(name="parent2")
        self.categ_kid1 = self.categ_root_2.add_child(name="kid1_parent2")
        self.categ_kid2 = self.categ_root_2.add_child(name="kid2_parent2")

        self.post_1 = PostFactory(
            status=Post.CurrentStatus.PUB.value, categ=self.categ_root_1
        )
        self.post_2 = PostFactory(
            status=Post.CurrentStatus.PUB.value, categ=self.categ_kid1
        )
        self.post_3 = PostFactory(
            status=Post.CurrentStatus.PUB.value, categ=self.categ_kid2
        )
        self.post_4 = PostFactory(
            categ=self.categ_kid2, status=Post.CurrentStatus.DRAFT.value
        )
        self.post_5 = PostFactory()  # default categ = unspecified
        self.post_6 = PostFactory(
            categ=self.categ_root_2, status=Post.CurrentStatus.PUB.value
        )
        self.client = Client()

    @override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
    def test_posts_categ_with_kids(self):
        """display public posts related to a given categ and it's decendants)"""
        path = reverse("posts:cat_search", kwargs={"slug": self.categ_root_2.slug})
        headers = {"HTTP_HX-Request": "true"}

        response = self.client.get(path, **headers)

        posts = response.context["posts"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(posts), 3)

    @override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
    def test_posts_categ_no_kids(self):
        """display public posts related to a given categ
        without decendants)"""
        categs_count = Category.objects.count()
        path = reverse("posts:cat_search", kwargs={"slug": self.categ_root_1.slug})

        response = self.client.get(path)

        posts = response.context["posts"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(posts), 1)
        self.assertEqual(categs_count, 5)


class PostSearchLangTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.post_1 = PostFactory.create(
            title_ru="Паралич Бэлла",
            content_ru="вирус герпеса, лечение преднизолоном,инфекциями",
            title_en="Bell's palsy",
            content_en="herpes virus, treatment,prednisone,infections",
            status=2,
        )

        self.post_2 = PostFactory(
            title_ru="Инфекция кожи",
            title_en="Skin infections",
            content_ru="Лечение чего-то там",
            content_en="Treatment",
            status=2,
        )
        self.post_3 = PostFactory(
            status=2,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )
        self.post_4 = PostFactory(
            status=0,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )
        self.post_5 = PostFactory(
            status=1,
            title_ru="Гипербиллирубинемия у новорождённых",
            content_ru="Фото терапия ",
            title_en="Newborns Hyperbilirubinemia",
            content_en="Photo therapy",
        )

    @override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
    def test_ru(self):
        """search in russian lang content"""
        url = reverse("posts:search_posts")

        search_word = "инфекция"
        data = {"q": search_word, "lang": "ru", "honeypot": ""}
        resp = self.client.get(url, data)

        posts = resp.context_data["posts"]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 2)

    @override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
    def test_not_public_ru(self):
        """results for posts only with status public"""
        url = reverse("posts:search_posts")

        search_word = "Гипербиллирубинемия"
        data = {"q": search_word, "lang": "ru", "honeypot": ""}
        resp = self.client.get(url, data)

        posts = resp.context_data["posts"]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 1)

    @override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
    def test_no_results_ru(self):
        """no search results in russian"""
        url = reverse("posts:search_posts")
        search_word = "квартирус"
        data = {"q": search_word, "lang": "ru", "honeypot": ""}
        resp = self.client.get(url, data)

        posts = resp.context_data["posts"]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 0)

    @override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
    def test_in_en(self):
        """search in english lang content"""
        url = reverse("posts:search_posts")
        search_word = "Hyperbilirubinemia"
        data = {"q": search_word, "lang": "en", "honeypot": ""}
        resp = self.client.get(url, data)

        posts = resp.context_data["posts"]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 1)

    @override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
    def test_no_results_en(self):
        """no results in english"""
        url = reverse("posts:search_posts")
        search_word = "kite"
        data = {"q": search_word, "lang": "en", "honeypot": ""}
        resp = self.client.get(url, data)

        posts = resp.context_data["posts"]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(posts), 0)


class PostDetailCommentsTestCase(TestCase):
    def setUp(self) -> None:
        self.post_1 = PostFactory(status=Post.CurrentStatus.PUB.value)
        self.post_2 = PostFactory(status=Post.CurrentStatus.PUB.value)
        self.user = UserFactory(username="tissa")
        self.comment_1 = CommentFactory(body="foo", post=self.post_1, user=self.user)
        self.comment_2 = CommentFactory(
            body="tired cat", post=self.post_1, user=self.user
        )
        self.comment_3 = CommentFactory(body="no fun", post=self.post_2, user=self.user)

    @override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
    def test_count_posts_comments(self):
        """comments for a given post;"""
        path = reverse("posts:post_detail", kwargs={"slug": self.post_1.slug})

        response = self.client.get(path)
        count_comments = response.context["comms_total"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_comments, 2)
