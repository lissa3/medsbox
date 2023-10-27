from django.db.models import Count
from django.test import TestCase, override_settings
from django.urls import reverse

from src.accounts.tests.factories import UserFactory
from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post
from src.posts.models.relation_model import Relation
from src.posts.tests.factories import CategoryFactory, PostFactory, RelationFactory


class CategoryPathTestCase(TestCase):
    def setUp(self) -> None:
        self.categ_root = CategoryFactory(name="grand_pa")

    def test_path_catges(self):
        """test model method get_full_path for categs"""

        self.categ_root.add_child(name="pa")
        parent = self.categ_root.get_last_child()
        parent.add_child(name="kid")
        kid = parent.get_first_child()
        categs_count_total = Category.objects.count()

        self.assertEqual(categs_count_total, 3)
        self.assertEqual(self.categ_root.get_children().count(), 1)
        self.assertEqual(self.categ_root.get_descendants().count(), 2)
        self.assertEqual(self.categ_root.get_full_path(), "grand_pa")
        self.assertEqual(parent.get_full_path(), "grand_pa/pa")
        self.assertEqual(kid.get_full_path(), "grand_pa/pa/kid")


@override_settings(LANGUAGE_CODE="ru", LANGUAGES=(("ru", "Russian"),))
class PostCreationTestCase(TestCase):
    def setUp(self) -> None:
        self.categ = CategoryFactory()

    def test_create_post_default_categ(self):
        """
        if post obj created without a categ it will be assigned to
        a default categ(name=="unspecified);
        if this categ does not exist it will be created
        """
        categs_initial_count = Category.objects.count()

        post_one = PostFactory.create()
        post_two = PostFactory.create()

        categ_one = Category.objects.get(id=post_one.categ.id)
        categ_two = Category.objects.get(id=post_two.categ.id)

        categs_final_count = Category.objects.count()

        self.assertEqual(categ_one.name, "Неопределена")
        self.assertEqual(categ_two.name, "Неопределена")
        self.assertEqual(categs_initial_count, 1)
        self.assertEqual(categs_final_count, 2)

    def test_create_post_with_categ(self):
        """
        post object gets assined category;
        one root categ is already present via factory
        """
        categs_initial_count = Category.objects.count()
        PostFactory.create(categ=self.categ)
        categs_final_count = Category.objects.count()

        self.assertEqual(categs_initial_count, 1)
        self.assertEqual(categs_final_count, 1)


class PostTagsTestCase(TestCase):
    def setUp(self) -> None:
        self.categ = CategoryFactory()
        self.post_1 = PostFactory.create(
            status=Post.CurrentStatus.PUB.value,
            tags=("антибиотики", "пневмония", "лихорадка"),
        )
        self.post_3 = PostFactory.create(
            status=Post.CurrentStatus.PUB.value, tags=("фарингит", "лихорадка")
        )
        self.post_4 = PostFactory.create(
            status=Post.CurrentStatus.PUB.value, tags=("пневмония", "лихорадка")
        )
        self.posts = PostFactory.create_batch(
            5, status=Post.CurrentStatus.PUB.value, tags=("пневмония",)
        )

    def test_similar_tags(self):
        """find posts with similar tags excl current post"""

        post_1_tags_ids = self.post_1.tags.values_list("id", flat=True)
        similar_posts = (
            Post.objects.get_public()
            .filter(tags__in=post_1_tags_ids)
            .exclude(id=self.post_1.id)
        )
        posts_annotated_tags = similar_posts.annotate(same_tags=Count("tags"))
        post_4_annot = posts_annotated_tags.filter(id=self.post_4.id).last()

        self.assertEqual(similar_posts.count(), 8)
        self.assertEqual(post_4_annot.same_tags, 2)


class UserInteractionTestCase(TestCase):
    def setUp(self) -> None:
        self.post = PostFactory(status=Post.CurrentStatus.PUB.value)
        self.user1 = UserFactory(username="zoo")
        self.user2 = UserFactory(username="lake")
        self.user3 = UserFactory(username="sky")
        RelationFactory(user=self.user1, post=self.post, in_bookmark=True, like=True)
        RelationFactory(user=self.user2, post=self.post, like=True, in_bookmark=True)
        RelationFactory(user=self.user3, post=self.post, like=True)

    def test_post_count_attrs(self):
        """check creation and update post calculated fields"""
        # self.post.refresh_from_db()
        post_likes = self.post.count_likes
        post_bmarks = self.post.count_bmarks

        self.assertEqual(post_likes, 3)
        self.assertEqual(post_bmarks, 2)
