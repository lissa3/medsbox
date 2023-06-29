from django.test import TestCase

from src.posts.models.categ_model import Category
from src.posts.tests.factories import CategoryFactory


class CategoryTestCase(TestCase):
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
