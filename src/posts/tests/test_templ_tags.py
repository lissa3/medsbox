from django.template import Context, Template
from django.test import TestCase

from src.posts.models.categ_model import Category


class CategsTempTagsTest(TestCase):
    """test custom inclusion tag for rendering nested categories"""

    TEMPLATE = Template("{% load categ_menu %} {% show_categs %}")

    def setUp(self):
        self.categ_root_1 = Category.add_root(name="apple")
        self.categ_root_2 = self.categ_root_1.add_sibling(name="sun")
        self.categ_kid_2 = self.categ_root_2.add_child(name="flower")

    def test_categs_shows(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn(self.categ_root_1.name, rendered)
        self.assertIn(self.categ_root_2.name, rendered)
        self.assertIn(self.categ_kid_2.name, rendered)
