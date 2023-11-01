from django.template import Context, Template
from django.test import TestCase, override_settings
from freezegun import freeze_time
from taggit.models import Tag

from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post
from src.posts.tests.factories import PostFactory


class CategsTempTagsTest(TestCase):
    """test custom inclusion tag for rendering nested categories"""

    TEMPLATE = Template("{% load sidebars %} {% show_categs %}")

    def setUp(self):
        self.categ_root_1 = Category.add_root(name="apple")
        self.categ_root_2 = self.categ_root_1.add_sibling(name="sun")
        self.categ_kid_2 = self.categ_root_2.add_child(name="flower")

    def test_categs_shows(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn(self.categ_root_1.name, rendered)
        self.assertIn(self.categ_root_2.name, rendered)
        self.assertIn(self.categ_kid_2.name, rendered)


class TagsInTempTest(TestCase):
    """
    test custom inclusion tag for rendering tags;
    tags only if they are linked to public posts
    """

    TEMPLATE = Template("{% load sidebars %} {% show_tags %}")

    def setUp(self):
        self.tag1 = Tag.objects.create(name="слон")
        self.tag2 = Tag.objects.create(name="глаз")
        self.tag3 = Tag.objects.create(name="кура")
        self.post_1 = PostFactory(
            status=Post.CurrentStatus.PUB.value, tags=(self.tag1,)
        )
        self.post_2 = PostFactory(
            status=Post.CurrentStatus.PUB.value, tags=(self.tag2,)
        )

    def test_tags_shows(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn(self.tag1.name, rendered)
        self.assertIn(self.tag2.name, rendered)
        self.assertNotIn(self.tag3.name, rendered)


@override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
class ArchiveTempTest(TestCase):
    TEMPLATE = Template("{% load calend %} {% show_archive %}")

    @freeze_time("2022-01-12")
    def setUp(self):
        self.post_1 = PostFactory(status=Post.CurrentStatus.PUB.value)
        self.post_2 = PostFactory(status=Post.CurrentStatus.PUB.value)

    @freeze_time("2023-05-23")
    def test_archive_show(self):
        PostFactory(status=Post.CurrentStatus.PUB.value)
        rendered = self.TEMPLATE.render(Context({}))

        self.assertIn(str(2022), rendered)
        self.assertIn(str(2023), rendered)
        self.assertIn("January", rendered)
        self.assertIn("May", rendered)
